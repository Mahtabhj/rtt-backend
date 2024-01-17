import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

import { Checkbox } from '@metronic-partials/controls';

import { Search } from '../Search/Search';

import './SelectAttributes.scss';

const propTypes = {
  values: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      value: PropTypes.string.isRequired,
    }),
  ).isRequired,
  attributes: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      field_type: PropTypes.string,
      list_values: PropTypes.string,
    }),
  ).isRequired,
  updateCallback: PropTypes.func.isRequired,
};

export const SelectAttributes = ({ values, attributes, updateCallback }) => {
  const [state, setState] = useState([]);

  useEffect(() => {
    const preparedValues = Object.fromEntries(values.map(({ id, value }) => [id, value]));

    const initialState = attributes.map(({ id }) => ({
      id,
      value: preparedValues[id] || '',
      isChecked: typeof preparedValues[id] === 'string',
    }));

    setState(initialState);
  }, [values, attributes]);

  const handleOnCheckboxSelect = attributeId => () => {
    const newState = state.map(attribute =>
      attribute.id === attributeId ? { ...attribute, isChecked: !attribute.isChecked } : attribute,
    );

    setState(newState);
    updateCallback(newState.filter(({ isChecked }) => isChecked));
  };

  const handleOnInputChange = attributeId => value => {
    const newState = state.map(attribute => (attribute.id === attributeId ? { ...attribute, value } : attribute));

    setState(newState);
    updateCallback(newState.filter(({ isChecked }) => isChecked));
  };

  const getCheckboxChecked = attributeId => state.find(({ id }) => id === attributeId)?.isChecked || false;

  const getInputValue = attributeId => state.find(({ id }) => id === attributeId)?.value || '';

  return (
    <div className="select-attributes">
      {attributes.length ? (
        attributes.map(({ id, name }) => (
          <div className="select-attributes__row" key={id}>
            <Checkbox isSelected={getCheckboxChecked(id)} onChange={handleOnCheckboxSelect(id)} />
            <span>{name}</span>
            <Search initialValue={getInputValue(id)} handleUpdateSearch={handleOnInputChange(id)} placeholder="" />
          </div>
        ))
      ) : (
        <span>no attributes available for selected R/RF</span>
      )}
    </div>
  );
};

SelectAttributes.propTypes = propTypes;
