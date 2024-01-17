import React, { useMemo } from 'react';
import PropTypes from 'prop-types';

import { headerFormatter } from '@metronic-helpers';

import { formatDateFullYear, ShortNameTooltip, REGION, REGULATION, REGULATORY_FRAMEWORK } from '@common';
import { getCheckboxesFilter, getDateFilter, getLimitFilter, getStatusFilter, getTextFilter } from '@common/Filters';
import { UiKitTable } from '@common/UIKit';

const headerStyle = { fontSize: '10px' };

const propTypes = {
  list: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      regions: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.number.isRequired,
          name: PropTypes.string.isRequired,
        }),
      ).isRequired,
      regulation: PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
      }),
      regulatory_framework: PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
      }),
      substance: PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        cas_no: PropTypes.string,
        ec_no: PropTypes.string,
      }),
      limit_attributes: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.number.isRequired,
          name: PropTypes.string.isRequired,
        }),
      ).isRequired,
      scope: PropTypes.string.isRequired,
      limit_value: PropTypes.number,
      measurement_limit_unit: PropTypes.string,
      limit_note: PropTypes.string,
      status: PropTypes.oneOf(['active', 'deleted']).isRequired,
      date_into_force: PropTypes.string,
      modified: PropTypes.string,
    }),
  ).isRequired,
  customOptions: PropTypes.object.isRequired,
  checkedIds: PropTypes.arrayOf(PropTypes.number.isRequired),
  setCheckedIds: PropTypes.func,
  onTableChangeCallback: PropTypes.func.isRequired,
};

const defaultProps = {
  checkedIds: [],
  setCheckedIds: null,
};

export const LimitTable = ({ list, customOptions, checkedIds, setCheckedIds, onTableChangeCallback }) => {
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
        dataField: 'regions',
        text: 'Region', // (comes from the R or RF of the limit record)
        sort: true,
        formatter: regions => regions.map(({ name }) => name).join(', '),
        headerFormatter,
        headerStyle,
        ...getCheckboxesFilter(REGION),
      },
      {
        dataField: 'regulation',
        text: 'Regulation', // name + ({regulation id})
        sort: true,
        formatter: (regulation, { id }) =>
          regulation ? (
            <ShortNameTooltip id={`regulation-${id}`} name={`${regulation.name} (ID: ${regulation.id})`} />
          ) : null,
        headerFormatter,
        headerStyle,
        style: { minWidth: '108px' },
        ...getCheckboxesFilter(REGULATION),
      },
      {
        dataField: 'regulatory_framework',
        text: 'Framework', // name + ({framework id})
        sort: true,
        formatter: (regulatory_framework, { id }) =>
          regulatory_framework ? (
            <ShortNameTooltip
              id={`regulatoryFramework-${id}`}
              name={`${regulatory_framework.name} (ID: ${regulatory_framework.id})`}
            />
          ) : null,
        headerFormatter,
        headerStyle,
        style: { minWidth: '108px' },
        ...getCheckboxesFilter(REGULATORY_FRAMEWORK),
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
        style: { maxWidth: '125px' },
        ...getTextFilter(),
      },
      {
        dataField: 'limit_attributes',
        text: 'Limit attributes', // string of Attribute names + attribute values
        sort: true,
        formatter: attributes => attributes.map(attribute => attribute.name).join(', '),
        headerFormatter,
        headerStyle,
      },
      {
        dataField: 'scope',
        text: 'Scope',
        sort: true,
        formatter: (scope, { id }) => (scope ? <ShortNameTooltip id={`scope-${id}`} name={scope} /> : null),
        headerFormatter,
        headerStyle,
        ...getTextFilter(),
      },
      {
        dataField: 'limit_value',
        text: 'Limit value',
        sort: true,
        headerFormatter,
        headerStyle,
        ...getLimitFilter(),
      },
      {
        dataField: 'measurement_limit_unit',
        text: 'Limit UoM',
        sort: true,
        headerFormatter,
        headerStyle,
      },
      {
        dataField: 'limit_note',
        text: 'Limit note',
        sort: true,
        formatter: (limitNote, { id }) =>
          limitNote ? <ShortNameTooltip id={`limitNote-${id}`} name={limitNote} /> : null,
        headerFormatter,
        headerStyle,
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
        dataField: 'date_into_force',
        text: 'Date into force',
        sort: true,
        formatter: formatDateFullYear,
        headerFormatter,
        headerStyle,
        ...getDateFilter(),
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

LimitTable.propTypes = propTypes;
LimitTable.defaultProps = defaultProps;
