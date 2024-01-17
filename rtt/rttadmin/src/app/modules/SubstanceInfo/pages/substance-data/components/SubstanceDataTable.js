import React, { useMemo } from 'react';
import PropTypes from 'prop-types';

import { headerFormatter } from '@metronic-helpers';

import { formatDateFullYear, ShortNameTooltip } from '@common';
import { getStatusFilter, getTextFilter } from '@common/Filters';
import { UiKitTable } from '@common/UIKit';

export const headerStyle = { fontSize: '10px' };

const propTypes = {
  list: PropTypes.arrayOf(PropTypes.shape({})).isRequired, // todo specify prop
  customOptions: PropTypes.object.isRequired,
  checkedIds: PropTypes.arrayOf(PropTypes.number.isRequired),
  setCheckedIds: PropTypes.func,
  onTableChangeCallback: PropTypes.func.isRequired,
};

const defaultProps = {
  checkedIds: [],
  setCheckedIds: null,
};

export const SubstanceDataTable = ({ list, customOptions, checkedIds, setCheckedIds, onTableChangeCallback }) => {
  const columns = useMemo(
    () => [
      {
        dataField: 'id',
        text: 'ID',
        sort: true,
        headerFormatter,
        headerStyle,
      },
      {
        dataField: 'substance',
        text: 'Substance', // name + ({substance CAS})  + ({substance EC})
        sort: true,
        formatter: (substance, { id }) =>
          substance ? (
            <ShortNameTooltip
              id={`substance-${id}`}
              name={`${substance.name} (CAS: ${substance.cas_no || '-'}) (EC: ${substance.ec_no || '-'})`}
            />
          ) : null,
        headerFormatter,
        headerStyle,
        style: { minWidth: '125px' },
        ...getTextFilter(),
      },
      {
        dataField: 'property',
        text: 'Property', // name + ({property id})
        sort: true,
        formatter: (property, { id }) =>
          property ? <ShortNameTooltip id={`property-${id}`} name={`${property.name} (ID: ${property.id})`} /> : null,
        headerFormatter,
        headerStyle,
        style: { minWidth: '108px' },
        ...getTextFilter(),
      },
      {
        dataField: 'property_data_point',
        text: 'Property data point', // name + ({property data point id})
        sort: true,
        formatter: (propertyDataPoint, { id }) =>
          propertyDataPoint ? (
            <ShortNameTooltip
              id={`propertyDataPoint-${id}`}
              name={`${propertyDataPoint.name} (ID: ${propertyDataPoint.id})`}
            />
          ) : null,
        headerFormatter,
        headerStyle,
        style: { minWidth: '108px' },
        ...getTextFilter(),
      },
      {
        dataField: 'value',
        text: 'Value',
        sort: true,
        headerFormatter,
        headerStyle,
        ...getTextFilter(),
      },
      {
        dataField: 'status',
        text: 'Status',
        sort: true,
        headerFormatter,
        headerStyle,
        ...getStatusFilter(),
      },
      {
        dataField: 'modified',
        text: 'Updated on',
        sort: true,
        formatter: formatDateFullYear,
        headerFormatter,
        headerStyle,
      },
    ],
    [],
  );

  return (
    <UiKitTable
      list={list}
      columns={columns}
      customOptions={customOptions}
      checkedIds={checkedIds}
      setCheckedIds={setCheckedIds}
      onTableChangeCallback={onTableChangeCallback}
    />
  );
};

SubstanceDataTable.propTypes = propTypes;
SubstanceDataTable.defaultProps = defaultProps;
