import React, { useState, useRef, useCallback } from 'react';
import { Overlay, Popover } from 'react-bootstrap';
import PropTypes from "prop-types";
import SVG from 'react-inlinesvg';
import cx from 'classnames';

import { OutsideClick } from '../../OutsideClick/OutsideClick';

import filter from './filter.svg';
import close from './close.svg';

import './FilterWrapper.scss';

const propTypes = {
  children: PropTypes.element.isRequired,
  filterId: PropTypes.string.isRequired,
  isDropButtonShown: PropTypes.bool,
  dropFilters: PropTypes.func,
  className: PropTypes.string,
};

const defaultProps = {
  isDropButtonShown: false,
  dropFilters: null,
  className: '',
};

const FilterWrapper = ({ children, filterId, isDropButtonShown, dropFilters, className }) => {
  const selectRef = useRef(null);

  const [isOpen, setOpen] = useState(false);

  const handleOnDrop = e => {
    e.stopPropagation();

    dropFilters && dropFilters();
  }

  const handleOnClose = useCallback(() => setOpen(false), []);

  const handleOnOpen = e => {
    e.stopPropagation();

    setOpen(!isOpen);
  }

  return (
    <div className={cx('filter-wrapper', className)} ref={selectRef}>
      {isDropButtonShown && (
        <SVG
          className="filter-wrapper__button filter-wrapper__button--absolute"
          onClick={handleOnDrop}
          src={close}
        />
      )}

      <SVG
        className="filter-wrapper__button"
        onClick={handleOnOpen}
        src={filter}
      />

      <Overlay
        show={isOpen}
        placement='bottom-end'
        target={selectRef.current}
      >
        <Popover
          id={`${filterId}-filter-popover`}
          className={cx('filter-wrapper__popover', className && `${className}__popover`)}
        >
          <Popover.Content>
            <OutsideClick onClickCallback={handleOnClose} isActive={isOpen}>
              {!!children && React.cloneElement(children, { ...children.props, onClose: handleOnClose })}
            </OutsideClick>
          </Popover.Content>
        </Popover>
      </Overlay>
    </div>
  );
};

FilterWrapper.propTypes = propTypes;
FilterWrapper.defaultProps = defaultProps;

export default FilterWrapper;
