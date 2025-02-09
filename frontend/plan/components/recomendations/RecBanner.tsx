import React, { useState } from "react";
import styled from "styled-components";
import RecHide from "./RecHide";
import RecInfo from "./RecInfo";
import RecNew from "./RecNew";
import { Icon } from "../bulma_derived_components";

const TIME_OUT_DURATION = 2000;

const BannerContainer = styled.div<{ collapse: boolean }>`
    display: flex;
    align-items: center;
    flex-direction: row;
    justify-content: space-between;
    margin-top: ${({ collapse }) => (collapse ? "1.5625rem" : "2.5rem")};
    margin-bottom: ${({ collapse }) => (collapse ? "0px" : "0.625rem")};
    transition: all 0.7s;
    padding: 0 0.9375rem;
`;

const BannerLeft = styled.span`
    display: flex;
    justify-content: space-around;
    align-items: center;
`;

const Title = styled.h3`
    font-weight: bold;
    padding: 0 0.5rem;
`;

const RefreshIcon = styled(Icon)`
    margin-left: 0.5rem;
    font-size: 0.75rem;
    margin-top: 0.125rem;
`;

const RefreshIconContainer = styled.span`
    line-height: 0.75rem;
    cursor: pointer;

    &:hover {
        ${RefreshIcon} {
            color: #4a4a4a !important;
        }
    }
`;

interface RecBannerProps {
    show: boolean;
    setShow: (_: boolean) => void;
    setRefresh: React.Dispatch<React.SetStateAction<boolean>>;
}

const RecBanner = ({ show, setShow, setRefresh }: RecBannerProps) => {
    const [refreshDisabled, setRefreshDisabled] = useState(false);

    // Cooldown of 2s after clicking refresh to prevent spamming
    const onRefresh = () => {
        setRefreshDisabled(true);
        setRefresh(true);

        setTimeout(function () {
            setRefreshDisabled(false);
        }, TIME_OUT_DURATION);
    };
    return (
        <BannerContainer collapse={!show}>
            {/* left side */}
            <BannerLeft>
                <RecNew />
                <Title>Recommended</Title>
                <RecInfo />
                <RefreshIconContainer
                    onClick={() => !refreshDisabled && onRefresh()}
                >
                    <RefreshIcon>
                        <i className="fa fa-sync fa-1x" aria-hidden="true" />
                    </RefreshIcon>
                </RefreshIconContainer>
            </BannerLeft>

            {/* Right side */}
            <span>
                <RecHide show={show} setShow={setShow} />
            </span>
        </BannerContainer>
    );
};

export default RecBanner;
