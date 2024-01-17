import React from 'react';
import PropTypes from 'prop-types';
// import dayjs from 'dayjs';

import { DateInput } from './DateInput/DateInput';

const propTypes = {
  selected: PropTypes.shape({
    from: PropTypes.string,
    to: PropTypes.string,
  }).isRequired,
  updateCallback: PropTypes.func.isRequired,
};

export const DateInputs = ({ selected, updateCallback }) => {

  const handleOnChange = ({ id, value }) => {
    if (value) {
      // const isoDate = (value.isBefore(dayjs()) ? value : dayjs()).toISOString();
      const isoDate = value.toISOString();

      if ((id === 'from' && value.isAfter(selected.to)) || (id === 'to' && value.isBefore(selected.from))) {
        updateCallback({ from: isoDate, to: isoDate})
      } else {
        updateCallback({ ...selected, [id]: isoDate });
      }
    } else {
      updateCallback({ ...selected, [id]: '' });
    }
  };

  return (
    <>
      <span>From</span>

      <DateInput
        id="from"
        value={selected.from}
        onChangeCallback={handleOnChange}
      />

      <span>To</span>

      <DateInput
        id="to"
        value={selected.to}
        onChangeCallback={handleOnChange}
      />
    </>
  );
};

DateInputs.propTypes = propTypes;
