import React, { useRef, useState } from "react";
import Async from "react-select/async";
import PropTypes from "prop-types";
import { debounce } from 'throttle-debounce';

import { getSubstancesDropdownData } from "@redux/commonApiService";

import { DEBOUNCE_TIMEOUT, TITLE_LIMIT_SHORT } from "../../constants";
import { shortTitleLength } from "../../utils";

const propTypes = {
  selected: PropTypes.array.isRequired,
  onChange: PropTypes.func.isRequired,
  isValuesShown: PropTypes.bool.isRequired,
  isSingle: PropTypes.bool,
  isDisabled: PropTypes.bool,
}

const defaultProps = {
  isSingle: false,
  isDisabled: false,
}

export const AddSubstanceManual = ({ selected, onChange, isValuesShown, isSingle, isDisabled }) => {
  const [searchInput, setSearchInput] = useState('');

  const debounceFunctionRef = useRef(
    debounce(DEBOUNCE_TIMEOUT, false, (inputValue, callback) =>
      inputValue.length > 3
        ? getSubstancesDropdownData(inputValue).then(results => callback(results.data)).catch(error => console.error(error))
        : callback([])
    )
  ).current;

  const loadSuggestedOptions = (inputValue, callback) => debounceFunctionRef(inputValue, callback);

  const handleOnChange = values => {
    onChange(values || []);
    setSearchInput('');
  };

  const renderOptionLabel = option => (
    <div className="d-flex">
      <span className="w-100" style={{ wordBreak: 'break-all' }}>
        {shortTitleLength(option.name, TITLE_LIMIT_SHORT)}
      </span>
      {searchInput ? (
        <div className="d-flex flex-column ml-3" style={{ minWidth: '145px' }}>
          <span>EC: {option.ec_no || '-'}</span>
          <span>CAS: {option.cas_no || '-'}</span>
        </div>
      ) : (
        <span className="ml-1">(EC: {option.ec_no || '-'}, CAS: {option.cas_no || '-'})</span>
      )}
    </div>
  );

  const renderOptionsMessage = () => searchInput.length > 3 ? "No results found" : "Enter more than 3 chars";

  return (
    <Async
      isMulti={!isSingle}
      inputValue={searchInput}
      onInputChange={setSearchInput}
      value={isValuesShown ? selected : []}
      onChange={handleOnChange}
      name="substances"
      getOptionLabel={renderOptionLabel}
      getOptionValue={option => option.id}
      loadOptions={loadSuggestedOptions}
      defaultOptions={[]}
      placeholder="Search by name, EC, CAS"
      noOptionsMessage={renderOptionsMessage}
      className="basic-multi-select"
      classNamePrefix="select"
      isDisabled={isDisabled}
      blurInputOnSelect
      captureMenuScroll
      closeMenuOnSelect
      cacheOptions
    />
  );
}

AddSubstanceManual.propTypes = propTypes;
AddSubstanceManual.defaultProps = defaultProps;
