import React, { useMemo } from 'react';
import PropTypes from 'prop-types';

import { headerFormatter } from '@metronic-helpers';

import { ShortNameTooltip } from '@common';
import { getTextFilter } from '@common/Filters';
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

export const FamilySubstancesTable = ({ list, customOptions, checkedIds, setCheckedIds, onTableChangeCallback }) => {
  const columns = useMemo(
    () => [
      {
        dataField: 'id',
        text: 'ID',
        headerFormatter,
        headerStyle,
      },
      {
        dataField: 'substance',
        text: 'Substance',
        formatter: (_, { id, name }) => (
          <ShortNameTooltip
            id={`substance-${id}`}
            name={name}
          />
        ),
        headerFormatter,
        headerStyle,
        style: { minWidth: '125px' },
        ...getTextFilter(),
      },
      {
        dataField: 'cas_no',
        text: 'CAS',
        headerFormatter,
        headerStyle,
        ...getTextFilter(),
      },
      {
        dataField: 'ec_no',
        text: 'EC',
        headerFormatter,
        headerStyle,
        ...getTextFilter(),
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

FamilySubstancesTable.propTypes = propTypes;
FamilySubstancesTable.defaultProps = defaultProps;
