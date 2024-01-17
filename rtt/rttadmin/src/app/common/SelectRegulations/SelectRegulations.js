import React, { useEffect, useRef, useState } from "react";
import { useDispatch } from "react-redux";
import Async from "react-select/async";
import PropTypes from "prop-types";

import { updateLastSelectedMultiTitle } from "@redux/app/appActions";
import { getRegulationDropdownData, getFrameworkDropdownData } from "@redux/commonApiService";

import { getCustomLabel } from "../utils";
import { debounce } from "throttle-debounce";
import { DEBOUNCE_TIMEOUT } from "../constants";

const getDropdownOptions = {
  regulations: getRegulationDropdownData,
  regulatory_frameworks: getFrameworkDropdownData,
}

const label = {
  regulations: 'Regulation',
  regulatory_frameworks: 'Regulatory Framework',
}

const propTypes = {
  selected: PropTypes.oneOfType([PropTypes.array, PropTypes.number]),
  onChange: PropTypes.func.isRequired,
  type: PropTypes.oneOf(['regulations', 'regulatory_frameworks']).isRequired,
  children: PropTypes.element,
  isDisabled: PropTypes.bool,
  isSingle: PropTypes.bool,
  isNameTooltip: PropTypes.bool,
}

const defaultProps = {
  selected: null,
  children: null,
  isDisabled: false,
  isSingle: false,
  isNameTooltip: false,
}

export const SelectRegulations = ({ selected, onChange, type, children, isDisabled, isSingle, isNameTooltip }) => {
  const dispatch = useDispatch();

  const [searchInput, setSearchInput] = useState('');
  const [options, setOptions] = useState([]);

  const debounceFunctionRef = useRef(
    debounce(DEBOUNCE_TIMEOUT, false, (inputValue, callback) => {
      if (['regulations', 'regulatory_frameworks'].includes(type)) {
        return getDropdownOptions[type](inputValue)
          .then(results => callback(results.data))
          .catch(error => console.error(error))
      } else {
        return callback([])
      }
    })
  ).current;

  const loadSuggestedOptions = (inputValue, callback) => debounceFunctionRef(inputValue, callback);

  useEffect(() => {
    let isSubscribed = true;

    if (['regulations', 'regulatory_frameworks'].includes(type)) {
      getDropdownOptions[type]('')
        .then(response => isSubscribed && setOptions(response.data))
        .catch(error => console.error(error));
    }

    return () => {
      isSubscribed = false
    }
  }, [type]);

  const handleOnChangeMulti = values => {
    dispatch(updateLastSelectedMultiTitle(values || []))
    onChange(values?.map(value => value.id) || []);
  };
  const handleOnChangeSingle = value => onChange(value.id);

  const getValueMulti = () => options.filter(option => (selected || []).includes(option.id));
  const getValueSingle = () => (options.find(option => selected === option.id) || null);

  const getOptionLabel = option => getCustomLabel(option, isNameTooltip);

  return (
    <div className="col-lg-6">
      <label>{`${label[type]}${isSingle ? '' : 's'}`}</label>
      <Async
        isMulti={!isSingle}
        inputValue={searchInput}
        onInputChange={setSearchInput}
        value={isSingle ? getValueSingle() : getValueMulti()}
        onChange={isSingle ? handleOnChangeSingle : handleOnChangeMulti}
        name={type}
        getOptionLabel={getOptionLabel}
        getOptionValue={option => option.id}
        loadOptions={loadSuggestedOptions}
        defaultOptions={options}
        noOptionsMessage={() => "No results found"}
        className="basic-multi-select"
        classNamePrefix="select"
        disabled={isDisabled}
        blurInputOnSelect
        captureMenuScroll
        closeMenuOnSelect
      />

      {children}
    </div>
  );
}

SelectRegulations.propTypes = propTypes;
SelectRegulations.defaultProps = defaultProps;
