import React from 'react';
import PropTypes from 'prop-types';
import DatePicker from 'react-datepicker';
import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat';

import './CustomDatePicker.scss';

// for IE11
dayjs.extend(customParseFormat);

const propTypes = {
  value: PropTypes.string,
  id: PropTypes.string.isRequired,
  onChangeCallback: PropTypes.func.isRequired,
};

const defaultProps = {
  value: '',
};

export const CustomDatePicker = ({ id, value, onChangeCallback }) => {
  const onChangeDate = (date, e) => {
    e.stopPropagation();

    onChangeCallback({ id, value: dayjs(date) });
  };

  return (
    <div className="custom-date-picker">
      <DatePicker
        selected={value ? dayjs(value).toDate() : new Date()}
        onChange={onChangeDate}
        // maxDate={new Date()}
        disabledKeyboardNavigation
        focusSelectedMonth
        inline
      />
    </div>
  );
};

CustomDatePicker.propTypes = propTypes;
CustomDatePicker.defaultProps = defaultProps;
