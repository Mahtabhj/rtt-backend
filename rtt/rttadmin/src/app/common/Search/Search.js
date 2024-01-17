import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';

import { DEBOUNCE_TIMEOUT, ENTER_KEYCODE } from '../constants';

const propTypes = {
  handleUpdateSearch: PropTypes.func.isRequired,
  initialValue: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  placeholder: PropTypes.string,
  type: PropTypes.oneOf(['text', 'number']),
};

const defaultProps = {
  initialValue: '',
  placeholder: 'Search...',
  type: 'text',
};

export const Search = ({ handleUpdateSearch, initialValue, placeholder, type }) => {
  const ref = useRef('');

  const [searchValue, setSearchValue] = useState('');
  const [debouncedValue, setDebouncedValue] = useState('');

  useEffect(() => {
    setSearchValue(initialValue);
    setDebouncedValue(initialValue);
  }, [initialValue]);

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(searchValue), DEBOUNCE_TIMEOUT);

    return () => clearTimeout(handler);
  }, [searchValue]);

  useEffect(() => {
    if (ref.current !== debouncedValue) {
      handleUpdateSearch(debouncedValue);

      ref.current = debouncedValue;
    }
  }, [ref, handleUpdateSearch, debouncedValue]);

  const handleOnChange = e => setSearchValue(e.target.value);

  const handleOnKeyDown = e => {
    if (e.keyCode === ENTER_KEYCODE) {
      const { value } = e.target;
      setSearchValue(value);
      setDebouncedValue(searchValue);
    }
  };

  return (
    <input
      type={type}
      className="form-control"
      placeholder={placeholder}
      onChange={handleOnChange}
      onKeyDown={handleOnKeyDown}
      value={searchValue}
    />
  );
};

Search.propTypes = propTypes;
Search.defaultProps = defaultProps;
