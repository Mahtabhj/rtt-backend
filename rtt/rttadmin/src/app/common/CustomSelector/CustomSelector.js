import React from 'react';
import cx from 'classnames';
import PropTypes from "prop-types";

import './CustomSelector.scss';

const propTypes = {
  options: PropTypes.array.isRequired,
  selected: PropTypes.string,
  setSelected: PropTypes.func.isRequired
};

export const CustomSelector = ({ options, selected, setSelected }) => {
  const handleOnSelect = e => {
    e.stopPropagation();
    const { value } = e.currentTarget.dataset;

    const newSelected = value === selected ? '' : value;

    setSelected(newSelected);
  };

  return (
    <div className="custom-selector">
      {options.map(option => (
        <div
          className={cx('custom-selector__option', { 'custom-selector__option--active': option === selected })}
          onClick={handleOnSelect}
          onKeyPress={handleOnSelect}
          data-value={option}
          role="button"
          tabIndex={0}
          key={option}
        >
          {option}
        </div>
      ))}
    </div>
  );
};

CustomSelector.propTypes = propTypes;
