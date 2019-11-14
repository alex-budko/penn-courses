import {
    CHANGE_SCHEDULE,
    CREATE_SCHEDULE,
    DELETE_SCHEDULE,
    REMOVE_SCHED_ITEM,
    RENAME_SCHEDULE,
    DUPLICATE_SCHEDULE,
    CLEAR_SCHEDULE,
    TOGGLE_CHECK,
    ADD_CART_ITEM,
    REMOVE_CART_ITEM,
    UPDATE_SCHEDULES,
    SET_SCHEDULE_ID,
    MARK_CART_SYNCED, MARK_SCHEDULE_SYNCED
} from "../actions";
import { meetingsContainSection } from "../meetUtil";

const DEFAULT_SCHEDULE_NAME = "Schedule";

// returns the default empty schedule
const generateDefaultSchedule = () => (
    {
        term: "2019A",
        meetings: [],
        colorPalette: [],
        LocAdded: false,
        pushedToBackend: true,
    }
);

// the state contains the following two pieces of data:
//  1. An object associating each schedule name with the schedule objecct
//  2. The name of the currently selected schedule
const initialState = {
    schedules: { [DEFAULT_SCHEDULE_NAME]: generateDefaultSchedule() },
    scheduleSelected: DEFAULT_SCHEDULE_NAME,
    cartSections: [],
    cartPushedToBackend: false,
};

/**
 * A helper method for removing a schedule from a schedules object
 * @param scheduleKey The name of the schedule
 * @param initialSchedule The initial schedules object
 */
const removeSchedule = (scheduleKey, initialSchedule) => {
    const newSchedules = {};
    Object.keys(initialSchedule)
        .filter(schedName => schedName !== scheduleKey)
        .forEach((schedName) => {
            newSchedules[schedName] = initialSchedule[schedName];
        });
    return newSchedules;
};

/**
 * Returns a new schedule where the section is present if it was not previously, and vice-versa
 * @param meetings
 * @param section
 */
const toggleSection = (meetings, section) => {
    if (meetingsContainSection(meetings, section)) {
        return meetings.filter(m => m.id !== section.id);
    }
    return [...meetings, section];
};

/**
 * Returns the next available schedule name that is similar to the given schedule name
 * Used for duplication
 * @param scheduleName: current schedule name
 * @param used: used schedule names stored in an object
 */
const nextAvailable = (scheduleName, used) => {
    let newScheduleName = scheduleName;
    // compute the current number at the end of the string (if it exists)
    let endNum = 0;
    let numDigits = 0;
    let selectionIndex = newScheduleName.length - 1;
    while (selectionIndex >= 0 && newScheduleName.charAt(selectionIndex) >= "0"
    && newScheduleName.charAt(selectionIndex) <= 9) {
        endNum += Math.pow(10, numDigits) * parseInt(newScheduleName.charAt(selectionIndex), 10);
        numDigits += 1;
        selectionIndex -= 1;
    }
    // prevent double arithmetic issues
    endNum = Math.round(endNum);
    // search for the next available number
    const baseName = newScheduleName.substring(0, newScheduleName.length - numDigits);
    while (used[newScheduleName]) {
        endNum += 1;
        newScheduleName = baseName + endNum;
    }
    return newScheduleName;
};

export const schedule = (state = initialState, action) => {
    const { cartSections } = state;
    switch (action.type) {
        case MARK_SCHEDULE_SYNCED:
            return {
                ...state,
                schedules: {
                    ...state.schedules,
                    [action.scheduleName]: {
                        ...state.schedules[action.scheduleName],
                        pushedToBackend: true,
                    }
                }
            };
        case MARK_CART_SYNCED:
            return {
                ...state,
                cartPushedToBackend: true,
            };
        case SET_SCHEDULE_ID:
            return {
                ...state,
                schedules: {
                    ...state.schedules,
                    [action.scheduleName]: {
                        ...state.schedules[action.scheduleName],
                        id: action.id,
                    },
                },
            };
        case UPDATE_SCHEDULES:
            // eslint-disable-next-line
            const { schedulesFromBackend } = action;
            // eslint-disable-next-line
            const newScheduleObject = { ...state.schedules };
            // eslint-disable-next-line
            const newCart = [...state.cartSections];
            let cartHasChanged = false;
            if (schedulesFromBackend) {
                schedulesFromBackend.forEach(({
                    id: scheduleId, name, sections, semester,
                }) => {
                    if (name === "cart") {
                        const oldSectionSet = {};
                        state.cartSections.forEach(({ id }) => {
                            oldSectionSet[id] = true;
                        });
                        sections.forEach((cartSection) => {
                            if (!oldSectionSet[cartSection.id]) {
                                newCart.push(cartSection);
                                cartHasChanged = true;
                            }
                        });
                    } else if (state.schedules[name]) {
                        newScheduleObject.schedules[name].pushedToBackend = false;
                        newScheduleObject.schedules[name].id = scheduleId;
                        const oldSectionSet = {};
                        state.schedules[name].meetings.forEach(({ id }) => {
                            oldSectionSet[id] = true;
                        });
                        sections.forEach((section) => {
                            if (!oldSectionSet[section.id]) {
                                newScheduleObject[name].meetings.push(section);
                            }
                        });
                    } else {
                        newScheduleObject[name] = {
                            meetings: sections,
                            semester,
                            pushedToBackend: true,
                        };
                    }
                });
            }
            return {
                ...state,
                schedules: newScheduleObject,
                cartSections: newCart,
                cartPushedToBackend: state.cartPushedToBackend && !cartHasChanged,
            };
        case CLEAR_SCHEDULE:
            return {
                ...state,
                schedules: {
                    ...state.schedules,
                    [state.scheduleSelected]: {
                        ...[state.scheduleSelected],
                        meetings: [],
                        cartPushedToBackend: false,
                    },
                },
            };
        case RENAME_SCHEDULE:
            return {
                ...state,
                schedules: {
                    ...removeSchedule(action.oldName, state.schedules),
                    [action.newName]: state.schedules[action.oldName],
                },
                scheduleSelected: state.scheduleSelected === action.oldName
                    ? action.newName : state.scheduleSelected,
            };
        case DUPLICATE_SCHEDULE:
            return {
                ...state,
                schedules: {
                    ...state.schedules,
                    [nextAvailable(action.scheduleName, state.schedules)]:
                        state.schedules[action.scheduleName],
                },
            };
        case CREATE_SCHEDULE:
            return {
                ...state,
                schedules: {
                    ...state.schedules,
                    [action.scheduleName]: generateDefaultSchedule(),
                },
                scheduleSelected: action.scheduleName,
            };
        case DELETE_SCHEDULE: {
            const newSchedules = removeSchedule(action.scheduleName, state.schedules);
            if (Object.keys(newSchedules).length === 0) {
                newSchedules["Empty Schedule"] = generateDefaultSchedule();
            }
            return {
                ...state,
                schedules: newSchedules,
                scheduleSelected: action.scheduleName === state.scheduleSelected
                    ? Object.keys(newSchedules)[0] : state.scheduleSelected,
            };
        }
        case CHANGE_SCHEDULE:
            return {
                ...state,
                scheduleSelected: action.scheduleId,
            };
        case TOGGLE_CHECK:
            return {
                ...state,
                schedules: {
                    ...state.schedules,
                    [state.scheduleSelected]: {
                        ...state[state.scheduleSelected],
                        meetings: toggleSection(state.schedules[state.scheduleSelected].meetings,
                            action.course),
                    },
                },
            };
        case REMOVE_SCHED_ITEM:
            return {
                ...state,
                schedules: {
                    ...state.schedules,
                    [state.scheduleSelected]: {
                        ...state[state.scheduleSelected],
                        meetings: state.schedules[state.scheduleSelected].meetings
                            .filter(m => m.id !== action.id),
                    },
                },
            };
        case ADD_CART_ITEM:
            return {
                ...state,
                cartSections: [...cartSections, action.section],
                cartPushedToBackend: false,
            };
        case REMOVE_CART_ITEM:
            return {
                ...state,
                cartSections: state.cartSections.filter(({ id }) => id !== action.sectionId),
                cartPushedToBackend: false,
            };
        default:
            return {
                ...state,
            };
    }
};
