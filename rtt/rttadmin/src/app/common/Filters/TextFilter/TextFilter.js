import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import PropTypes from 'prop-types';

import { isDroppingFiltersSelector } from '@redux/app/appSelectors';

import FilterWrapper from '../FilterWrapper/FilterWrapper';
import { Search } from '../../Search/Search';

import './TextFilter.scss';

const propTypes = {
  onSelect: PropTypes.func.isRequired,
};

export const TextFilter = ({ onSelect }) => {

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
  };

  return (
    <FilterWrapper
      className="text-filter-wrapper"
      filterId="text"
      isDropButtonShown={!!selected}
      dropFilters={handleDropFilters}
    >
      <div className="text-filter">
        <Search
          initialValue={selected}
          handleUpdateSearch={handleOnSelect}
          placeholder=''
        />
      </div>
    </FilterWrapper>
  );
};

TextFilter.propTypes = propTypes;
