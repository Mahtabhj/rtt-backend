import React, { useEffect, useMemo } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import * as actions from "@redux-regulation/issuingbody/issuingbodyActions";
import * as uiHelpers from "../IssuingBodyUIHelpers";
import {
  getSelectRow,
  getHandlerTableChange,
  NoRecordsFoundMessage,
  PleaseWaitMessage,
} from "@metronic-helpers";
import * as columnFormatters from "./column-formatters";
import { useIssuingBodyUIContext } from "../IssuingBodyUIContext";

export function IssuingBodyTable() {
  const issuingbodyUIContext = useIssuingBodyUIContext();

  const issuingbodyUIProps = useMemo(() => {
    return {
      ids: issuingbodyUIContext.ids,
      setIds: issuingbodyUIContext.setIds,
      queryParams: issuingbodyUIContext.queryParams,
      setQueryParams: issuingbodyUIContext.setQueryParams,
      openEditIssuingBodyPage: issuingbodyUIContext.openEditIssuingBodyPage,
      openSelectIssuingBodyPage: issuingbodyUIContext.openSelectIssuingBodyPage,
      openDeleteIssuingBodyDialog:
        issuingbodyUIContext.openDeleteIssuingBodyDialog,
    };
  }, [issuingbodyUIContext]);

  // Getting curret state of issuingbody list from store (Redux)
  const { currentState } = useSelector(
    (state) => ({ currentState: state.issuingbody }),
    shallowEqual
  );

  const { totalCount, entities } = currentState;

  // IssuingBody Redux state
  const dispatch = useDispatch();

  useEffect(() => {
    // clear selections list
    issuingbodyUIProps.setIds([]);

    // server call by queryParams
    dispatch(actions.fetchIssuingBodyList(issuingbodyUIProps.queryParams));

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [issuingbodyUIProps.queryParams, dispatch]);

  // Table columns
  const columns = [
    {
      dataField: "name",
      text: "IssuingBody Name",
      sort: true,
    },
    {
      dataField: "description",
      text: "Description",
      sort: true,
    },
    {
      dataField: "region",
      text: "Region",
      sort: true,
      formatter: (cellContent) => cellContent?.name,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditIssuingBodyPage: issuingbodyUIProps.openEditIssuingBodyPage,
        openSelectIssuingBodyPage: issuingbodyUIProps.openSelectIssuingBodyPage,
        openDeleteIssuingBodyDialog:
          issuingbodyUIProps.openDeleteIssuingBodyDialog,
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  const pageListRenderer = ({ pages, onPageChange }) => {
    // just exclude <, <<, >>, >
    const pageWithoutIndication = pages.filter(
      (p) => typeof p.page !== "string"
    );
    return (
      <div className="position-absolute" style={{ right: "1rem" }}>
        {pageWithoutIndication.map((p) => (
          <button
            className="btn btn-primary ml-1 pt-2 pb-2 pr-3 pl-3"
            onClick={() => onPageChange(p.page)}
          >
            {p.page}
          </button>
        ))}
      </div>
    );
  };

  const paginationOptions = {
    totalSize: totalCount,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <PaginationProvider pagination={paginationFactory(paginationOptions)}>
        {({ paginationTableProps }) => {
          return (
            <BootstrapTable
              wrapperClasses="table-responsive"
              classes="table table-head-custom table-vertical-center overflow-hidden"
              remote
              bootstrap4
              bordered={false}
              keyField="id"
              data={entities === null ? [] : entities}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={getHandlerTableChange(
                issuingbodyUIProps.setQueryParams
              )}
              selectRow={getSelectRow({
                entities,
                ids: issuingbodyUIProps.ids,
                setIds: issuingbodyUIProps.setIds,
              })}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={entities} />
              <NoRecordsFoundMessage entities={entities} />
            </BootstrapTable>
          );
        }}
      </PaginationProvider>
    </>
  );
}
