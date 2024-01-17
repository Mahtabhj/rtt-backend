import React from 'react';
import PropTypes from 'prop-types';
import { ErrorMessage } from 'formik';

const propTypes = {
  name: PropTypes.string.isRequired,
};

export const UiKitErrorMessage = ({ name }) => (
  <ErrorMessage name={name}>
    {(msg) => <div style={{ marginBottom: '-20px', height: '20px', color: '#e7576c' }}>{msg}</div>}
  </ErrorMessage>
);

UiKitErrorMessage.propTypes = propTypes;
