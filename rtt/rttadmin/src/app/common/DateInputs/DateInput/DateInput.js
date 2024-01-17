import React, { useState, useRef, useCallback } from 'react';
import PropTypes from 'prop-types';
import { FormControl, Overlay, Popover } from 'react-bootstrap';
import MaskedInput from "react-maskedinput";
import dayjs from "dayjs";

import { OutsideClick } from "../../OutsideClick/OutsideClick";

import { CustomDatePicker } from "../CustomDatePicker/CustomDatePicker";

import { DATE_FORMAT } from "../../constants";

import './DateInput.scss';

const propTypes = {
  value: PropTypes.string,
  id: PropTypes.string.isRequired,
  onChangeCallback: PropTypes.func.isRequired,
};

const defaultProps = {
  value: null,
};

export const DateInput = ({ id, value, onChangeCallback }) => {
  const popupTargetRef = useRef(null);

  const [isPopupOpen, setPopupOpen] = useState(false);

  const handleOnClickInput = e => {
    e.stopPropagation();

    setPopupOpen(!isPopupOpen);
  }

  const handleOnClickOutside = useCallback(() => setPopupOpen(false), []);

  const handleOnChangeMaskedInput = e => {
    const { id, value } = e.target;

    const date = dayjs(value, DATE_FORMAT);

    if (value) {
      if (date.isValid()) {
        onChangeCallback({ id, value: date });
      }
    } else {
      onChangeCallback({ id, value: '' });
    }
  }

  return (
    <div>
      <OutsideClick isActive={isPopupOpen} onClickCallback={handleOnClickOutside}>
        <div ref={popupTargetRef}>
          <div className="date-input">
            <FormControl
              as={MaskedInput}
              onChange={handleOnChangeMaskedInput}
              onClick={handleOnClickInput}
              id={id}
              placeholder={DATE_FORMAT}
              value={dayjs(value).format(DATE_FORMAT)}
              type="text"
              mask="11/11/11"
              autoComplete="off"
            />
          </div>

          <Overlay
            show={isPopupOpen}
            placement='bottom'
            target={popupTargetRef.current}
            container={popupTargetRef.current}
          >
            <Popover id={id} className="date-input-popover">
              <Popover.Content>
                <CustomDatePicker
                  id={id}
                  value={value}
                  onChangeCallback={onChangeCallback}
                />
              </Popover.Content>
            </Popover>
          </Overlay>
        </div>
      </OutsideClick>
    </div>
  );
};

DateInput.propTypes = propTypes;
DateInput.defaultProps = defaultProps;
