import fetch from "cross-fetch";
import getCsrf from "../csrf";

export const UPDATE_SEARCH = "UPDATE_SEARCH";
export const UPDATE_SEARCH_REQUEST = "UPDATE_SEARCH_REQUEST";

export const UPDATE_COURSE_INFO_SUCCESS = "UPDATE_COURSE_INFO_SUCCESS";
export const UPDATE_COURSE_INFO_REQUEST = "UPDATE_COURSE_INFO_REQUEST";

export const UPDATE_SECTIONS = "UPDATE_SECTIONS";
export const OPEN_SECTION_INFO = "OPEN_SECTION_INFO";
export const CHANGE_SCHEDULE = "CHANGE_SCHEDULE";
export const CREATE_SCHEDULE = "CREATE_SCHEDULE";

export const OPEN_MODAL = "OPEN_MODAL";
export const CLOSE_MODAL = "CLOSE_MODAL";

export const ADD_SCHED_ITEM = "ADD_SCHED_ITEM";
export const REMOVE_SCHED_ITEM = "REMOVE_SCHED_ITEM";
export const DELETE_SCHEDULE = "DELETE_SCHEDULE";
export const RENAME_SCHEDULE = "RENAME_SCHEDULE";
export const DUPLICATE_SCHEDULE = "DUPLICATE_SCHEDULE";
export const CLEAR_SCHEDULE = "CLEAR_SCHEDULE";

export const COURSE_SEARCH_ERROR = "COURSE_SEARCH_ERROR";
export const COURSE_SEARCH_LOADING = "COURSE_SEARCH_LOADING";
export const COURSE_SEARCH_SUCCESS = "COURSE_SEARCH_SUCCESS";

export const LOAD_REQUIREMENTS = "LOAD_REQUIREMENTS";
export const ADD_SCHOOL_REQ = "ADD_SCHOOL_REQ";
export const REM_SCHOOL_REQ = "REM_SCHOOL_REQ";
export const UPDATE_SEARCH_TEXT = "UPDATE_SEARCH_TEXT";

export const UPDATE_RANGE_FILTER = "UPDATE_RANGE_FILTER";
export const CLEAR_FILTER = "CLEAR_FILTER";
export const CLEAR_ALL = "CLEAR_ALL";

export const SECTION_INFO_SEARCH_ERROR = "SECTION_INFO_SEARCH_ERROR";
export const SECTION_INFO_SEARCH_LOADING = "SECTION_INFO_SEARCH_LOADING";
export const SECTION_INFO_SEARCH_SUCCESS = "SECTION_INFO_SEARCH_SUCCESS";

export const TOGGLE_CHECK = "TOGGLE_CHECK";

export const ADD_CART_ITEM = "ADD_CART_ITEM";
export const REMOVE_CART_ITEM = "REMOVE_CART_ITEM";
export const CHANGE_SORT_TYPE = "CHANGE_SORT_TYPE";

// Backend accounts integration
export const UPDATE_SCHEDULES = "UPDATE_SCHEDULES";
export const SET_SCHEDULE_ID_MARK_SYNCED = "SET_SCHEDULE_ID_MARK_SYNCED";
export const MARK_SCHEDULE_SYNCED = "MARK_SCHEDULE_SYNCED";
export const MARK_CART_SYNCED = "MARK_CART_SYNCED";


export const markScheduleSynced = scheduleName => (
    {
        scheduleName,
        type: MARK_SCHEDULE_SYNCED,
    }
);

export const markCartSynced = () => (
    {
        type: MARK_CART_SYNCED,
    }
);

export const duplicateSchedule = scheduleName => (
    {
        type: DUPLICATE_SCHEDULE,
        scheduleName,
    }
);

export const deleteSchedule = scheduleName => (
    {
        type: DELETE_SCHEDULE,
        scheduleName,
    }
);

export const renameSchedule = (oldName, newName) => (
    {
        type: RENAME_SCHEDULE,
        oldName,
        newName,
    }
);

export const changeSchedule = scheduleId => (
    {
        type: CHANGE_SCHEDULE,
        scheduleId,
    }
);

export const addSchedItem = section => (
    {
        type: ADD_SCHED_ITEM,
        section,
    }
);

export const addCartItem = section => (
    {
        type: ADD_CART_ITEM,
        section,
    }
);

export const removeSchedItem = id => (
    {
        type: REMOVE_SCHED_ITEM,
        id,
    }
);

export const updateSearch = searchResults => (
    {
        type: UPDATE_SEARCH,
        searchResults,
    }
);

const updateSearchRequest = () => (
    {
        type: UPDATE_SEARCH_REQUEST,
    }
);

export const updateSections = sections => (
    {
        type: UPDATE_SECTIONS,
        sections,
    }
);

export const updateSectionInfo = sectionInfo => (
    {
        type: OPEN_SECTION_INFO,
        sectionInfo,
    }
);

const updateCourseInfoRequest = () => (
    {
        type: UPDATE_COURSE_INFO_REQUEST,
    }
);

export const updateCourseInfo = course => (
    {
        type: UPDATE_COURSE_INFO_SUCCESS,
        course,
    }
);

export const createScheduleOnFrontend = scheduleName => (
    {
        type: CREATE_SCHEDULE,
        scheduleName,
    }
);

export const openModal = (modalKey, modalProps, modalTitle) => (
    {
        type: OPEN_MODAL,
        modalKey,
        modalProps,
        modalTitle,
    }
);


export const closeModal = () => (
    {
        type: CLOSE_MODAL,
    }
);

export const clearSchedule = () => (
    {
        type: CLEAR_SCHEDULE,
    }
);

export const loadRequirements = () => (
    dispatch => (
        fetch("/requirements")
            .then(
                response => response.json()
                    .then((data) => {
                        const obj = {
                            SAS: [],
                            SEAS: [],
                            WH: [],
                            NURS: [],
                        };
                        const selObj = {};
                        data.forEach((element) => {
                            obj[element.school].push(element);
                            selObj[element.id] = 0;
                        });
                        dispatch({
                            type: LOAD_REQUIREMENTS,
                            obj,
                            selObj,
                        });
                    }, (error) => {
                        // eslint-disable-next-line no-console
                        console.log(error);
                    }),
                (error) => {
                    // eslint-disable-next-line no-console
                    console.log(error);
                }
            )
    )
);

function buildCourseSearchUrl(filterData) {
    let queryString = `/courses/?search=${filterData.searchString}`;

    // Requirements filter
    const reqs = [];
    if (filterData.selectedReq) {
        for (const key of Object.keys(filterData.selectedReq)) {
            if (filterData.selectedReq[key] === 1) {
                reqs.push(key);
            }
        }

        if (reqs.length > 0) {
            queryString += `&requirements=${reqs[0]}`;
            for (let i = 1; i < reqs.length; i += 1) {
                queryString += `,${reqs[i]}`;
            }
        }
    }

    // Range filters
    const filterFields = ["difficulty", "course_quality", "instructor_quality", "cu"];
    const defaultFilters = [[0, 4], [0, 4], [0, 4], [0.5, 2]];
    for (let i = 0; i < filterFields.length; i += 1) {
        if (filterData[filterFields[i]]
            && JSON.stringify(filterData[filterFields[i]]) !== JSON.stringify(defaultFilters[i])) {
            const filterRange = filterData[filterFields[i]];
            queryString += `&${filterFields[i]}=${filterRange[0]}-${filterRange[1]}`;
        }
    }

    return queryString;
}

export function fetchCourseSearch(filterData) {
    return (dispatch) => {
        dispatch(updateSearchRequest());
        fetch(buildCourseSearchUrl(filterData))
            .then(
                response => response.json()
                    .then(
                        json => dispatch(updateSearch(json)),
                        error => dispatch(courseSearchError(error)),
                    ),
                error => dispatch(courseSearchError(error)),
            );
    };
}

export function updateSearchText(s) {
    return {
        type: UPDATE_SEARCH_TEXT,
        s,
    };
}

function buildSectionInfoSearchUrl(searchData) {
    return `/courses/${searchData.param}`;
}


export function courseSearchError(error) {
    return {
        type: COURSE_SEARCH_ERROR,
        error,
    };
}

export function sectionInfoSearchError(error) {
    return {
        type: SECTION_INFO_SEARCH_ERROR,
        error,
    };
}

export function addSchoolReq(reqID) {
    return {
        type: ADD_SCHOOL_REQ,
        reqID,
    };
}

export function remSchoolReq(reqID) {
    return {
        type: REM_SCHOOL_REQ,
        reqID,
    };
}

export function updateRangeFilter(field, values) {
    return {
        type: UPDATE_RANGE_FILTER,
        field,
        values,
    };
}

export function clearFilter(propertyName) {
    return {
        type: CLEAR_FILTER,
        propertyName,
    };
}


export function clearAll() {
    return {
        type: CLEAR_ALL,
    };
}

export const updateSchedules = schedulesFromBackend => ({
    type: UPDATE_SCHEDULES,
    schedulesFromBackend,
});

export function fetchCourseDetails(courseId) {
    return (dispatch) => {
        dispatch(updateCourseInfoRequest());
        fetch(`/courses/${courseId}`)
            .then(res => res.json())
            .then(course => dispatch(updateCourseInfo(course)))
            .catch(error => dispatch(sectionInfoSearchError(error)));
    };
}

/**
 * Pulls schedules from the backend
 * If the cart isn't included, it creates a cart
 * @param cart The courses in the cart
 * @param onComplete The function to call when initialization has been completed (with the schedules
 * from the backend)
 * @returns {Function}
 */
export const fetchSchedulesAndInitializeCart = (cart, onComplete = () => null) => (dispatch) => {
    fetch("/schedules/")
        .then(res => res.json())
        .then(schedules => {
            if (schedules) {
                dispatch(updateSchedules(schedules));
            }
            if (!schedules.cart) {
                dispatch(createScheduleOnBackend("cart", cart));
            }
            onComplete(schedules);
        })
        .catch(error => console.log(error, "Not logged in"));
};

export const setScheduleIdAndMarkSynced = (name, id) => ({
    type: SET_SCHEDULE_ID_MARK_SYNCED,
    name,
    id,
});

/**
 * Creates a schedule on the backend
 * @param name The name of the schedule
 * @param sections The list of sections for the schedule
 * @returns {Function}
 */
export const createScheduleOnBackend = (name, sections) => (dispatch) => {
    fetch("/schedules/", {
        method: "POST",
        credentials: "include",
        mode: "same-origin",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrf()
        },
        body: JSON.stringify({
            name,
            sections,
        }),
    })
        .then(response => {
            if (response.ok) {
                response.json()
                    .then(({ id }) => {
                        if (id) {
                            dispatch(setScheduleIdAndMarkSynced(name, id));
                        }
                    });
            }
        })
        .catch(ignored => null);
};

/**
 * Updates a schedule on the backend
 * Skips if the id is not yet initialized for the schedule
 * Once the schedule has been updated, the schedule is marked as updated locally
 * @param name The name of the schedule
 * @param schedule The schedule object
 */
export const updateScheduleOnBackend = (name, schedule) => (dispatch) => {
    const { id } = schedule;
    if (!id) {
        return;
    }
    const updatedScheduleObj = {
        ...schedule,
        name,
        sections: schedule.meetings,
    };
    return fetch(`/schedules/${id}/`, {
        method: "PUT",
        credentials: "include",
        mode: "same-origin",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrf(),
        },
        body: JSON.stringify(updatedScheduleObj),
    })
        .then(() => {
            if (name === "cart") {
                dispatch(markCartSynced());
            } else {
                dispatch(markScheduleSynced(name));
            }
        })
        .catch(() => {
        });
};

export function fetchSectionInfo(searchData) {
    return dispatch => (
        fetch(buildSectionInfoSearchUrl(searchData))
            .then(
                response => response.json()
                    .then(
                        (json) => {
                            const info = {
                                id: json.id,
                                description: json.description,
                                crosslistings: json.crosslistings,
                            };
                            const { sections } = json;
                            dispatch(updateCourseInfo(sections, info));
                        },
                        error => dispatch(sectionInfoSearchError(error)),
                    ),
                error => dispatch(sectionInfoSearchError(error)),
            )
    );
}

export function courseSearchLoading() {
    return {
        type: COURSE_SEARCH_LOADING,
    };
}

export function courseSearchSuccess(items) {
    return {
        type: COURSE_SEARCH_SUCCESS,
        items,
    };
}

export const toggleCheck = course => ({
    type: TOGGLE_CHECK,
    course,
});

export const removeCartItem = sectionId => ({
    type: REMOVE_CART_ITEM,
    sectionId,
});

export const changeSortType = sortMode => ({
    type: CHANGE_SORT_TYPE,
    sortMode,
});
