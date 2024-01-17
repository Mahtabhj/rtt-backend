import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import PropTypes from 'prop-types';

import { isDroppingFiltersSelector } from '@redux/app/appSelectors';

import FilterWrapper from '../FilterWrapper/FilterWrapper';
import { Search } from '../../Search/Search';

import './LimitFilter.scss';

const initialSelected = { min: '', max: '' };

const propTypes = {
  onSelect: PropTypes.func.isRequired
};

export const LimitFilter = ({ onSelect }) => {

  const [selected, setSelected] = useState(initialSelected);

  const isDroppingFilters = useSelector(isDroppingFiltersSelector);

  useEffect(() => {
    if (isDroppingFilters) {
      setSelected(initialSelected);
    }
  }, [isDroppingFilters]);
  
  const isDropButtonShown = selected.min !== '' && selected.max !== '';

  const handleDropFilters = () => {
    setSelected(initialSelected);
    onSelect(null);
  }

  const handleUpdateMin = value => {
    const newSelected = { min: value >=0 ? value : 0, max: selected.max };

    setSelected(newSelected);

    if (value <= selected.max) {
      onSelect(newSelected);
    }
  };

  const handleUpdateMax = value => {
    const newSelected = { min: selected.min, max: value >=0 ? value : 0 };

    setSelected(newSelected);

    if (value >= selected.max) {
      onSelect(newSelected);
    }
  };

  return (
    <FilterWrapper
      className="limit-filter-wrapper"
      filterId="limit"
      isDropButtonShown={isDropButtonShown}
      dropFilters={handleDropFilters}
    >
      <div className="limit-filter">
        <span className="limit-filter__from">From</span>
        <Search
          type="number"
          initialValue={selected.min}
          handleUpdateSearch={handleUpdateMin}
          placeholder=''
        />
        <span className="limit-filter__to">To</span>
        <Search
          type="number"
          initialValue={selected.max}
          handleUpdateSearch={handleUpdateMax}
          placeholder=''
        />
      </div>
    </FilterWrapper>
  );
};

LimitFilter.propTypes = propTypes;
