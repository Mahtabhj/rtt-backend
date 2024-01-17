import React, { useMemo } from 'react';
import PropTypes from 'prop-types';

import { headerFormatter } from '@metronic-helpers';

import { formatDateFullYear, ShortNameTooltip, REGION, REGULATION, REGULATORY_FRAMEWORK } from '@common';
import { getCheckboxesFilter, getDateFilter, getStatusFilter, getTextFilter } from '@common/Filters';
import { UiKitTable } from '@common/UIKit';

const headerStyle = { fontSize: '10px' };

const propTypes = {
  list: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
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
      }).isRequired,
      article: PropTypes.string.isRequired,
      reference: PropTypes.string,
      application: PropTypes.string.isRequired,
      expiration_date: PropTypes.string,
      date_into_force: PropTypes.string,
      status: PropTypes.oneOf(['active', 'deleted']).isRequired,
      modified: PropTypes.string.isRequired,
      regions: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.number.isRequired,
          name: PropTypes.string.isRequired,
        }),
      ).isRequired,
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

export const ExemptionTable = ({ list, customOptions, checkedIds, setCheckedIds, onTableChangeCallback }) => {
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
        style: { minWidth: '125px' },
        ...getTextFilter(),
      },
      {
        dataField: 'article',
        text: 'Article/annex',
        sort: true,
        headerFormatter,
        headerStyle,
        ...getTextFilter(),
      },
      {
        dataField: 'reference',
        text: 'Reference',
        sort: true,
        headerFormatter,
        headerStyle,
      },
      {
        dataField: 'application',
        text: 'Application',
        sort: true,
        formatter: (application, { id }) =>
          application ? <ShortNameTooltip id={`application-${id}`} name={application} /> : null,
        headerFormatter,
        headerStyle,
        style: { minWidth: '125px' },
      },
      {
        dataField: 'expiration_date',
        text: 'Expiration date',
        sort: true,
        formatter: formatDateFullYear,
        headerFormatter,
        headerStyle,
        ...getDateFilter(),
      },
      {
        dataField: 'date_into_force',
        text: 'Date entry into force',
        sort: true,
        formatter: formatDateFullYear,
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

ExemptionTable.propTypes = propTypes;
ExemptionTable.defaultProps = defaultProps;
