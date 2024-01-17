import React, { useCallback, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';
import { FormCheck } from 'react-bootstrap';

import { isDroppingFiltersSelector } from '@redux/app/appSelectors';

import {
  getRegulationFilterOptions,
  getRegulatoryFrameworkFilterOptions,
  getRegionFilterOptions
} from '../../../modules/LimitInfo/_redux/filters/filtersActions';
import { filtersSelector } from '../../../modules/LimitInfo/_redux/filters/filtersSelectors';

import { REGION, REGULATION, REGULATORY_FRAMEWORK, Search } from '../../';

import FilterWrapper from '../FilterWrapper/FilterWrapper';

import './CheckboxesFilter.scss';

const getFilterOptions = {
  [REGULATION]: getRegulationFilterOptions,
  [REGULATORY_FRAMEWORK]: getRegulatoryFrameworkFilterOptions,
  [REGION]: getRegionFilterOptions,
}

const propTypes = {
  onSelect: PropTypes.func.isRequired,
  type: PropTypes.oneOf([REGULATION, REGULATORY_FRAMEWORK, REGION]).isRequired
};

export const CheckboxesFilter = ({ onSelect, type }) => {
  const dispatch = useDispatch();

  const [selectedId, setSelectedId] = useState(null);
  const [searchInput, setSearchInput] = useState('');

  const options = useSelector(filtersSelector)[type];

  const isDroppingFilters = useSelector(isDroppingFiltersSelector);

  useEffect(() => {
    if (isDroppingFilters) {
      setSelectedId(null);
    }
  }, [isDroppingFilters]);

  const fetchOptions = useCallback(() => {
    dispatch(getFilterOptions[type](searchInput))
  }, [dispatch, type, searchInput]);

  useEffect(() => {
    fetchOptions();
  }, [fetchOptions]);

  const handleOnInputChange = value => setSearchInput(value);

  const handleOnCheck = ({ currentTarget: { id, name } }) => {
    const newSelected = selectedId === id ? null : { id, name };

    setSelectedId(newSelected?.id || null);
    onSelect(newSelected?.name || null);
  };

  const handleDropFilters = () => {
    setSelectedId(null);
    onSelect(null);
  };

  return (
    <FilterWrapper
      className="checkboxes-filter-wrapper"
      filterId="checkboxes"
      isDropButtonShown={!!selectedId}
      dropFilters={handleDropFilters}
    >
      <div className="checkboxes-filter">
        <Search initialValue={searchInput} handleUpdateSearch={handleOnInputChange} placeholder='' />

        <div className="checkboxes-filter__options">
          {options.length ? (
            options.map(option => (
              <FormCheck
                type="checkbox"
                checked={option.id === +selectedId}
                onChange={handleOnCheck}
                label={<span>{option.name}</span>}
                name={option.name}
                key={option.id}
                id={option.id}
                custom
                inline
              />
            ))
          ) : (
            <div className="checkboxes-filter__no-results">No results</div>
          )}
        </div>
      </div>
    </FilterWrapper>
  );
};

CheckboxesFilter.propTypes = propTypes;
