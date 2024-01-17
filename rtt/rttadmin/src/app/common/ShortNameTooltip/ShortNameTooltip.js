import React, { useEffect, useRef, useState } from 'react';
import { useDispatch, useSelector } from "react-redux";
import { OverlayTrigger, Tooltip } from 'react-bootstrap';
import PropTypes from 'prop-types';
import cx from 'classnames';

import { setOpenTooltipId } from "@redux/app/appActions";
import { openTooltipIdSelector } from "@redux/app/appSelectors";

import { shortTitleLength } from '../utils';
import { TITLE_LIMIT_ULTRASHORT, TOOLTIP_DELAY } from '../constants';

import { OutsideClick } from "../OutsideClick/OutsideClick";

import './ShortNameTooltip.scss';

const propTypes = {
  id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]).isRequired,
  name: PropTypes.string.isRequired,
  isAutoHide: PropTypes.bool,
  isModalTooltip: PropTypes.bool,
};

const defaultProps = {
  isAutoHide: false,
  isModalTooltip: false,
};

export const ShortNameTooltip = ({ id, name, isAutoHide, isModalTooltip }) => {
  const shortName = shortTitleLength(name, TITLE_LIMIT_ULTRASHORT);
  const tooltipId = `short-name-tooltip-${id}`;

  const dispatch = useDispatch();

  const openTooltipId = useSelector(openTooltipIdSelector);

  const tooltipTargetRef = useRef(null);
  const [isTooltipShown, setTooltipShown] = useState(false);

  useEffect(() => {
    if (!isAutoHide && openTooltipId && openTooltipId !== tooltipId) {
      setTooltipShown(false);
    }
  }, [isAutoHide, tooltipId, openTooltipId]);

  const handleOnToggle = () => {
    if (!isTooltipShown) {
      setTooltipShown(true);

      if (!isAutoHide) {
        dispatch(setOpenTooltipId(tooltipId));
      }
    }
  }
  const handleOnClickOutside = () => setTooltipShown(false);

  const renderTooltip = props => (
    <Tooltip
      className={cx('short-name-tooltip', { 'short-name-modal-tooltip': isModalTooltip })}
      id={tooltipId}
      {...props}
    >
      <span className="short-name-tooltip-inner">{name}</span>
    </Tooltip>
  );

  if (shortName?.length === name?.length) {
    return name;
  }

  return isAutoHide ? (
    <OverlayTrigger
      placement="top"
      delay={{ show: TOOLTIP_DELAY, hide: TOOLTIP_DELAY }}
      overlay={renderTooltip}
      key={id}
    >
      <span>{shortName}</span>
    </OverlayTrigger>
  ) : (
    <OutsideClick isActive={isTooltipShown} onClickCallback={handleOnClickOutside}>
      <div ref={tooltipTargetRef}>
        <OverlayTrigger
          show={isTooltipShown}
          onToggle={handleOnToggle}
          placement="top"
          delay={{ show: TOOLTIP_DELAY, hide: TOOLTIP_DELAY }}
          container={tooltipTargetRef.current}
          overlay={renderTooltip}
        >
          <span>{shortName}</span>
        </OverlayTrigger>
      </div>
    </OutsideClick>
  );
};

ShortNameTooltip.propTypes = propTypes;
ShortNameTooltip.defaultProps = defaultProps;
