import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import PropTypes from 'prop-types';

import { isDroppingFiltersSelector } from '@redux/app/appSelectors';

import { CustomSelector } from '../../CustomSelector/CustomSelector';
import FilterWrapper from '../FilterWrapper/FilterWrapper';

import './SelectFilter.scss';

const propTypes = {
  options: PropTypes.array.isRequired,
  onSelect: PropTypes.func.isRequired
};

export const SelectFilter = ({ options, onSelect }) => {

  const [selected, setSelected] = useState('');

  const isDroppingFilters = useSelector(isDroppingFiltersSelector);

  useEffect(() => {
    if (isDroppingFilters) {
      setSelected('');
    }
  }, [isDroppingFilters]);
  
  const handleOnSelect = value => {
    setSelected(value);
    onSelect(value);
  };

  const handleDropFilters = () => {
    setSelected('');
    onSelect(null);
  }

  return (
    <FilterWrapper
      className="select-filter-wrapper"
      filterId="select"
      isDropButtonShown={!!selected}
      dropFilters={handleDropFilters}
    >
      <CustomSelector options={options} selected={selected} setSelected={handleOnSelect} />
    </FilterWrapper>
  );
};

SelectFilter.propTypes = propTypes;
