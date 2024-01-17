import React, { useMemo } from "react";
import PropTypes from "prop-types";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

import { getSelectRow, pageListRenderer } from "@metronic-helpers";

const propTypes = {
  substances: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    ec_no: PropTypes.string,
    cas_no: PropTypes.string,
    organization: PropTypes.arrayOf(PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
    })),
  })).isRequired,
  customOptions: PropTypes.object,
  checkedIds: PropTypes.arrayOf(PropTypes.number.isRequired),
  setCheckedIds: PropTypes.func,
  onTableChangeCallback: PropTypes.func,
};

const defaultProps = {
  customOptions: null,
  checkedIds: [],
  setCheckedIds: null,
  onTableChangeCallback: null,
};

export function SubstancesTable({ substances, customOptions, checkedIds, setCheckedIds, onTableChangeCallback}) {
  const columns = useMemo(() => {
    const columns = [
      {
        dataField: "ec_no",
        text: "EC Number",
        sort: true,
      },
      {
        dataField: "cas_no",
        text: "CAS Number",
        sort: true,
      },
      {
        dataField: "name",
        text: "Substance Name",
        sort: true,
        style: { maxWidth: '450px' },
      },
      {
        dataField: "organization",
        text: "Organizations",
        sort: true,
        style: { minWidth: '120px' },
        formatter: cellContent => (
          <div className="d-flex flex-column">
            {!!cellContent?.length && cellContent.map(item => <span key={item.id}>{item.name}</span>)}
          </div>
        ),
      },
    ];

    return setCheckedIds
      ? [
          {
            dataField: "id",
            text: "ID",
            sort: true,
          },
          ...columns
        ]
      : columns;
  }, [setCheckedIds]);

  const options = {
    sizePerPage: 10,
    hideSizePerPage: true,
    showTotal: true,
    paginationTotalRenderer: (from, to, size) => (
      <span className="react-bootstrap-table-pagination-total ml-5">
        Showing { from } to { to } of { size } substances
      </span>
    ),
    pageListRenderer,
    ...customOptions,
  };

  if (!substances?.length || typeof substances[0] !== 'object') return (<></>);

  return (
    <BootstrapTable
      wrapperClasses="table-responsive"
      bordered={false}
      classes="table table-head-custom table-vertical-center overflow-hidden"
      bootstrap4
      keyField="id"
      data={substances}
      columns={columns}
      pagination={paginationFactory(options)}
      selectRow={{
        ...getSelectRow({
          entities: substances,
          ids: checkedIds,
          setIds: setCheckedIds,
        }),
        hideSelectColumn: !setCheckedIds,
        clickToSelect: false,
      }}
      onTableChange={onTableChangeCallback}
      remote={{ pagination: !!onTableChangeCallback }}
    />
  );
}

SubstancesTable.propTypes = propTypes;
SubstancesTable.defaultProps = defaultProps;
