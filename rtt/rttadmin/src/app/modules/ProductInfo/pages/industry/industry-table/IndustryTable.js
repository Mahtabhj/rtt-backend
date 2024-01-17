import {
  getHandlerTableChange,
  getSelectRow,
  NoRecordsFoundMessage,
  pageListRenderer,
  PleaseWaitMessage,
} from "@metronic-helpers";
import * as actions from "@redux-product/industry/industryActions";
import React, { useEffect, useMemo } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { useIndustryUIContext } from "../IndustryUIContext";
import * as uiHelpers from "../IndustryUIHelpers";
import * as columnFormatters from "./column-formatters";

export function IndustryTable() {
  // Industry UI Context
  const industryUIContext = useIndustryUIContext();

  const industryUIProps = useMemo(() => {
    return {
      ids: industryUIContext.ids,
      setIds: industryUIContext.setIds,
      queryParams: industryUIContext.queryParams,
      setQueryParams: industryUIContext.setQueryParams,
      openEditIndustryPage: industryUIContext.openEditIndustryPage,
      openSelectIndustryPage: industryUIContext.openSelectIndustryPage,
      openDeleteIndustryDialog: industryUIContext.openDeleteIndustryDialog,
    };
  }, [industryUIContext]);

  // Getting curret state of industry list from store (Redux)
  const { currentState } = useSelector(
    (state) => ({ currentState: state.industry }),
    shallowEqual
  );

  const { totalCount, entities } = currentState;

  // Industry Redux state
  const dispatch = useDispatch();

  useEffect(() => {
    // clear selections list
    industryUIProps.setIds([]);

    // server call by queryParams
    dispatch(actions.fetchIndustryList(industryUIProps.queryParams));

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [industryUIProps.queryParams, dispatch]);

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },
    {
      dataField: "name",
      text: "Name",
      sort: true,
    },
    {
      dataField: "description",
      text: "Description",
      sort: true,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditIndustryPage: industryUIProps.openEditIndustryPage,
        openDeleteIndustryDialog: industryUIProps.openDeleteIndustryDialog,
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
                industryUIProps.setQueryParams
              )}
              selectRow={getSelectRow({
                entities,
                ids: industryUIProps.ids,
                setIds: industryUIProps.setIds,
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
