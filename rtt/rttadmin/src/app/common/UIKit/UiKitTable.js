import React from 'react';
import PropTypes from 'prop-types';
import BootstrapTable from 'react-bootstrap-table-next';
import filterFactory  from 'react-bootstrap-table2-filter';
import paginationFactory from 'react-bootstrap-table2-paginator';

import { getSelectRow, pageListRenderer } from '@metronic-helpers';

const propTypes = {
  list: PropTypes.arrayOf(PropTypes.object).isRequired,
  columns: PropTypes.arrayOf(PropTypes.shape({
    dataField: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired,
    sort: PropTypes.bool,
    formatter: PropTypes.func,
    headerFormatter: PropTypes.func,
    headerStyle: PropTypes.object,
    style: PropTypes.object,
  })).isRequired,
  customOptions: PropTypes.object.isRequired,
  checkedIds: PropTypes.arrayOf(PropTypes.number.isRequired),
  setCheckedIds: PropTypes.func,
  onTableChangeCallback: PropTypes.func.isRequired,
};

const defaultProps = {
  checkedIds: [],
  setCheckedIds: null,
};

export const UiKitTable = ({ list, columns, customOptions, checkedIds, setCheckedIds, onTableChangeCallback }) => {
  const options = {
    sizePerPage: 10,
    hideSizePerPage: true,
    showTotal: true,
    pageListRenderer,
    ...customOptions,
  };

  return (
    <BootstrapTable
      wrapperClasses="table-responsive"
      bordered={false}
      classes="table table-head-custom table-vertical-center overflow-hidden"
      bootstrap4
      keyField="id"
      data={list}
      columns={columns}
      pagination={paginationFactory(options)}
      filter={filterFactory()}
      onTableChange={onTableChangeCallback}
      remote={{ pagination: true }}
      selectRow={{
        ...getSelectRow({
          entities: list,
          ids: checkedIds,
          setIds: setCheckedIds,
          isCheckboxClickOnly: true,
        }),
        hideSelectColumn: !setCheckedIds,
        clickToSelect: false
      }}
    />
  );
}

UiKitTable.propTypes = propTypes;
UiKitTable.defaultProps = defaultProps;
