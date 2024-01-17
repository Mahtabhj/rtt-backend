import React from 'react';
import { ProgressBar } from 'react-bootstrap';
import PropTypes from 'prop-types';

const propTypes = {
  variant: PropTypes.oneOf(['success', 'query']),
  isLoading: PropTypes.bool.isRequired,
};

const defaultProps = {
  variant: 'success',
};

export const UiKitProgressBar = ({ variant, isLoading }) =>
  isLoading && (
    <div className="position-relative">
      <ProgressBar
        className="position-absolute"
        variant={variant}
        animated
        now={100}
        style={{ height: '3px', width: '100%' }}
      />
    </div>
  );

UiKitProgressBar.propTypes = propTypes;
UiKitProgressBar.defaultProps = defaultProps;
