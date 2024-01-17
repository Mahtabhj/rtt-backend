import React from 'react';
import PropTypes from 'prop-types';

import { BUTTON } from '../constants';

const getButton = {
  [BUTTON.SAVE]: (onClick, isLoading) => (
    <button
      className="btn btn-primary btn-elevate"
      type="submit"
      onClick={onClick}
      disabled={isLoading}
      style={{ width: '100px' }}
    >
      Save
      {isLoading && <span className="ml-3 spinner spinner-white" />}
    </button>
  ),
  [BUTTON.CANCEL]: (onClick, isLoading) => (
    <button className="btn btn-light btn-elevate" type="button" onClick={onClick} disabled={isLoading}>
      Cancel
    </button>
  ),
};

const propTypes = {
  buttonType: PropTypes.oneOf([BUTTON.SAVE, BUTTON.CANCEL]).isRequired,
  onClick: PropTypes.func.isRequired,
  isLoading: PropTypes.bool,
};

const defaultProps = {
  isLoading: false,
};

export const UiKitButton = ({ onClick, buttonType, isLoading }) => getButton[buttonType](onClick, isLoading);

UiKitButton.propTypes = propTypes;
UiKitButton.defaultProps = defaultProps;
