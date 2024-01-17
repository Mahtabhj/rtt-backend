import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import SVG from 'react-inlinesvg';

import starIcon from './starIcon.svg';

import './RatingStars.scss';

const STARS_COUNT = 5;

const propTypes = {
  rating: PropTypes.number,
  className: PropTypes.string,
  setRating: PropTypes.func,
};

const defaultProps = {
  rating: 0,
  className: '',
  setRating: null,
};

export const RatingStars = ({ rating, className, setRating }) => {
  const array = Array.from({ length: STARS_COUNT }, (v, i) => (rating > i ? 1 : 0));

  const handleChangeRating = ({ currentTarget: { dataset } }) => setRating(dataset.rate === rating ? 0 : dataset.rate);

  return (
    <div className={cx('rating-stars', className)}>
      {array.map((star, index) => (
        <SVG
          onClick={handleChangeRating}
          className={cx(
            'rating-stars__star',
            { 'rating-stars__star--fill': !!star },
            { 'rating-stars__star--clickable': setRating },
          )}
          key={`${star}${index}`}
          src={starIcon}
          data-rate={index + 1}
        />
      ))}
    </div>
  );
};

RatingStars.propTypes = propTypes;
RatingStars.defaultProps = defaultProps;
