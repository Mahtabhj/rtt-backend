import React, { useCallback, useEffect, useState } from "react";
import Async from "react-select/async";
import PropTypes from "prop-types";
import { ErrorMessage } from "formik";

import { getIssuingBodyDropdownData } from "@redux/commonApiService";

import { getCustomLabel } from "../utils";

const propTypes = {
  selectedId: PropTypes.number,
  onChange: PropTypes.func.isRequired,
}

const defaultProps = {
  selectedId: null,
}

export const SelectIssuingBody = ({ selectedId, onChange }) => {
  const [searchInput, setSearchInput] = useState('');
  const [options, setOptions] = useState([]);

  const handleLoadOptions = useCallback(() => {
    return getIssuingBodyDropdownData(searchInput)
      .then(response => response.data.results)
      .catch(error => console.error(error))
  }, [searchInput]);

  useEffect(() => {
    let isSubscribed = true;

    getIssuingBodyDropdownData()
      .then(response => isSubscribed && setOptions(response.data.results))
      .catch(error => console.error(error))

    return () => {
      isSubscribed = false
    }
  }, []);

  return (
    <div className="col-lg-6">
      <label>Issuing Body *</label>
      <Async
        name="issuing_body"
        value={options.find(option => option.id === selectedId)}
        inputValue={searchInput}
        onInputChange={setSearchInput}
        onChange={onChange}
        getOptionLabel={getCustomLabel}
        getOptionValue={option => option.id}
        loadOptions={handleLoadOptions}
        defaultOptions={options}
        noOptionsMessage={() => "No results found"}
        blurInputOnSelect
        captureMenuScroll
        closeMenuOnSelect
      />
      <ErrorMessage name="issuing_body">
        {(msg) => <div style={{ color: "red" }}>{msg}</div>}
      </ErrorMessage>
    </div>
  );
}

SelectIssuingBody.propTypes = propTypes;
SelectIssuingBody.defaultProps = defaultProps;
