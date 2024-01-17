import React, { useCallback } from 'react';
import PropTypes from 'prop-types';

import { DataPointItem } from './DataPointItem';

const propTypes = {
  values: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string,
      value: PropTypes.string,
      status: PropTypes.oneOf(['active', 'deleted']),
      modified: PropTypes.string,
      image: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
      isChecked: PropTypes.bool,
    }),
  ).isRequired,
  updateCallback: PropTypes.func.isRequired,
};

export const PropertyDataPoints = ({ values, updateCallback }) => {
  const updateItemCallback = useCallback(
    updatingItem =>
      updateCallback(values.map(dataPoint => (dataPoint.id === updatingItem.id ? updatingItem : dataPoint))),
    [values, updateCallback],
  );

  return values.length ? (
    values.map(item => <DataPointItem item={item} updateItemCallback={updateItemCallback} key={item.id} />)
  ) : (
    <div className="mt-3">no property data points available</div>
  );
};

PropertyDataPoints.propTypes = propTypes;
