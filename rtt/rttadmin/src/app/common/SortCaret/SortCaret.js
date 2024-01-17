import React from 'react';
import SVG from 'react-inlinesvg';
import PropTypes from 'prop-types';

import asc from './images/asc.svg';
import desc from './images/desc.svg';

import './SortCaret.scss';

const propTypes = {
  order: PropTypes.oneOf(['asc', 'desc']).isRequired,
}

export const SortCaret = ({ order }) => (
  <SVG className="sort-caret" src={order === 'asc' ? asc : desc} />
)

SortCaret.propTypes = propTypes