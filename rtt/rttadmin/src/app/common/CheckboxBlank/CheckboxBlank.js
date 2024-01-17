import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

import './CheckboxBlank.scss';

const propTypes = {
  isSelected: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired,
  type: PropTypes.oneOf(['yellow', 'green']).isRequired,
  className: PropTypes.string
};

const defaultProps = {
  className: '',
}

export const CheckboxBlank = ({ isSelected, onClick, type, className }) => (
  <div
    className={cx(className, 'checkbox-blank', `checkbox-blank--${type}`, {'checkbox-blank--selected': isSelected})}
    role="button"
    onClick={onClick}
    onKeyPress={onClick}
    tabIndex={0}
  />
);

CheckboxBlank.propTypes = propTypes;
CheckboxBlank.defaultProps = defaultProps;
