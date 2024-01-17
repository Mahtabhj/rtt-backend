import React, { useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

const propTypes = {
  children: PropTypes.node.isRequired,
  onClickCallback: PropTypes.func.isRequired,
  isActive: PropTypes.bool.isRequired,
  className: PropTypes.string,
};

const defaultProps = {
  className: '',
};

export const OutsideClick = ({ children, onClickCallback, isActive, className }) => {
  const wrapperRef = useRef();

  useEffect(() => {
    const handleClickOutside = e => {
      if (isActive && !wrapperRef.current?.contains(e.target)) {
        onClickCallback();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onClickCallback, isActive]);

  return (
    <div className={cx('outside-click-wrapper', className)} ref={wrapperRef}>
      {children}
    </div>
  );
};

OutsideClick.propTypes = propTypes;
OutsideClick.defaultProps = defaultProps;
