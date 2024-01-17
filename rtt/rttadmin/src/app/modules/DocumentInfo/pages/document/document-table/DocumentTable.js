import {
  getHandlerTableChange,
  getSelectRow,
  NoRecordsFoundMessage,
  pageListRenderer,
  PleaseWaitMessage,
} from "@metronic-helpers";
import * as actions from "@redux-document/document/documentActions";
import React, { useEffect, useMemo } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { useDocumentUIContext } from "../DocumentUIContext";
import * as uiHelpers from "../DocumentUIHelpers";
import * as columnFormatters from "./column-formatters";

export function DocumentTable() {
  // Document UI Context
  const documentUIContext = useDocumentUIContext();

  const documentUIProps = useMemo(() => {
    return {
      ids: documentUIContext.ids,
      setIds: documentUIContext.setIds,
      queryParams: documentUIContext.queryParams,
      setQueryParams: documentUIContext.setQueryParams,
      openEditDocumentPage: documentUIContext.openEditDocumentPage,
      openSelectDocumentPage: documentUIContext.openSelectDocumentPage,
      openDeleteDocumentDialog: documentUIContext.openDeleteDocumentDialog,
    };
  }, [documentUIContext]);

  // Getting curret state of document list from store (Redux)
  const { currentState } = useSelector(
    (state) => ({
      currentState: state.document,
    }),
    shallowEqual
  );

  const { totalCount, entities } = currentState;

  // Document Redux state
  const dispatch = useDispatch();

  useEffect(() => {
    // clear selections list
    documentUIProps.setIds([]);

    // server call by queryParams
    dispatch(actions.fetchDocumentList(documentUIProps.queryParams));

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [documentUIProps.queryParams, dispatch]);

  // Table columns
  const columns = [
    {
      dataField: "type",
      text: "Type",
      sort: true,
      formatter: (cellContent) => cellContent?.name,
    },
    {
      dataField: "title",
      text: "Name",
      sort: true,
    },
    {
      dataField: "description",
      text: "Found in",
      sort: true,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditDocumentPage: documentUIProps.openEditDocumentPage,
        openSelectDocumentPage: documentUIProps.openSelectDocumentPage,
        openDeleteDocumentDialog: documentUIProps.openDeleteDocumentDialog,
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  // Table pagination properties
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
        {({ paginationProps, paginationTableProps }) => {
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
                documentUIProps.setQueryParams
              )}
              selectRow={getSelectRow({
                entities,
                ids: documentUIProps.ids,
                setIds: documentUIProps.setIds,
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
