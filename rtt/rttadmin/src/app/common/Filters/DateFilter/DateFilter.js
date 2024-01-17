import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import PropTypes from 'prop-types';

import { isDroppingFiltersSelector } from '@redux/app/appSelectors';

import FilterWrapper from '../FilterWrapper/FilterWrapper';

import { DateInputs } from '../../DateInputs/DateInputs';

import './DateFilter.scss';

const initialSelected = { from: '', to: '' };

const propTypes = {
  onSelect: PropTypes.func.isRequired
};

export const DateFilter = ({ onSelect }) => {

  const [selected, setSelected] = useState(initialSelected);

  const isDroppingFilters = useSelector(isDroppingFiltersSelector);

  useEffect(() => {
    if (isDroppingFilters) {
      setSelected(initialSelected);
    }
  }, [isDroppingFilters]);
  
  const isDropButtonShown = !!selected.from && !!selected.to;

  const handleDropFilters = () => {
    setSelected(initialSelected);
    onSelect(null);
  }

  const handleUpdateSelected = ({ from, to }) => {
    setSelected({ from, to });
    from && to && onSelect({ from, to });
  }

  return (
    <FilterWrapper
      className="date-filter-wrapper"
      filterId="date"
      isDropButtonShown={isDropButtonShown}
      dropFilters={handleDropFilters}
    >
      <div className="date-filter">
        <DateInputs selected={selected} updateCallback={handleUpdateSelected} />
      </div>
    </FilterWrapper>
  );
};

DateFilter.propTypes = propTypes;
