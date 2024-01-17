import React from 'react';
import PropTypes from 'prop-types';

import { getBoolString } from "../utils";

const propTypes = {
  options: PropTypes.arrayOf(PropTypes.string.isRequired).isRequired,
  selected: PropTypes.string.isRequired,
  onSelect: PropTypes.func.isRequired,
};

export const TabMenu = ({ options, selected, onSelect }) => {
  const handleChangeTab = e => {
    const { value } = e.currentTarget.dataset;
    onSelect(value);
  };

  return (
    <ul className="nav nav-tabs nav-tabs-line " role="tablist">
      {options.map(option => (
        <li className="nav-item" data-value={option} onClick={handleChangeTab} key={option}>
          <a
            className={`nav-link ${selected === option && "active"}`}
            data-toggle="tab"
            role="tab"
            aria-selected={getBoolString(selected === option)}
          >
            {option}
          </a>
        </li>
      ))}
    </ul>
  );
};

TabMenu.propTypes = propTypes;
