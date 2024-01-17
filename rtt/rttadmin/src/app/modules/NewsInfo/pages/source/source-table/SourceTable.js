import {
  getHandlerTableChange,
  getSelectRow,
  NoRecordsFoundMessage,
  pageListRenderer,
  PleaseWaitMessage,
} from "@metronic-helpers";
import * as actions from "@redux-news/source/sourceActions";
import React, { useEffect, useMemo } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { useSourceUIContext } from "../SourceUIContext";
import * as uiHelpers from "../SourceUIHelpers";
import * as columnFormatters from "./column-formatters";

export function SourceTable() {
  // Source UI Context
  const sourceUIContext = useSourceUIContext();

  const sourceUIProps = useMemo(() => {
    return {
      ids: sourceUIContext.ids,
      setIds: sourceUIContext.setIds,
      queryParams: sourceUIContext.queryParams,
      setQueryParams: sourceUIContext.setQueryParams,
      openEditSourcePage: sourceUIContext.openEditSourcePage,
      openSelectSourcePage: sourceUIContext.openSelectSourcePage,
      openDeleteSourceDialog: sourceUIContext.openDeleteSourceDialog,
    };
  }, [sourceUIContext]);

  // Getting curret state of source list from store (Redux)
  const { currentState } = useSelector(
    (state) => ({
      currentState: state.source,
    }),
    shallowEqual
  );

  const { totalCount, entities } = currentState;

  // Source Redux state
  const dispatch = useDispatch();

  useEffect(() => {
    // clear selections list
    sourceUIProps.setIds([]);

    // server call by queryParams
    dispatch(actions.fetchSourceList(sourceUIProps.queryParams));

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sourceUIProps.queryParams, dispatch]);

  // Table columns
  const columns = [
    {
      dataField: "name",
      text: "Name",
      sort: true,
    },
    {
      dataField: "link",
      text: "Source",
      sort: true,
    },
    {
      dataField: "type.name",
      text: "Type",
      sort: true,
    },
    {
      dataField: "news_source",
      text: "News",
      sort: true,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditSourcePage: sourceUIProps.openEditSourcePage,
        openSelectSourcePage: sourceUIProps.openSelectSourcePage,
        openDeleteSourceDialog: sourceUIProps.openDeleteSourceDialog,
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
                sourceUIProps.setQueryParams
              )}
              selectRow={getSelectRow({
                entities,
                ids: sourceUIProps.ids,
                setIds: sourceUIProps.setIds,
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
