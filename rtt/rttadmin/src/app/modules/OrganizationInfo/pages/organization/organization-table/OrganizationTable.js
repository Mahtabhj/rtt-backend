import {
  getHandlerTableChange,
  getSelectRow,
  NoRecordsFoundMessage,
  pageListRenderer,
  PleaseWaitMessage,
} from "@metronic-helpers";
import * as actions from "@redux-organization/organization/organizationActions";
import React, { useEffect, useMemo } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { useOrganizationUIContext } from "../OrganizationUIContext";
import * as uiHelpers from "../OrganizationUIHelpers";
import * as columnFormatters from "./column-formatters";

export function OrganizationTable() {
  // Organization UI Context
  const organizationUIContext = useOrganizationUIContext();

  const organizationUIProps = useMemo(() => {
    return {
      ids: organizationUIContext.ids,
      setIds: organizationUIContext.setIds,
      queryParams: organizationUIContext.queryParams,
      setQueryParams: organizationUIContext.setQueryParams,
      openEditOrganizationPage: organizationUIContext.openEditOrganizationPage,
      openSelectOrganizationPage:
        organizationUIContext.openSelectOrganizationPage,
      openDeleteOrganizationDialog:
        organizationUIContext.openDeleteOrganizationDialog,
    };
  }, [organizationUIContext]);

  // Getting curret state of organization list from store (Redux)
  const { currentState } = useSelector(
    (state) => ({ currentState: state.organization }),
    shallowEqual
  );

  const { totalCount, entities } = currentState;

  // Organization Redux state
  const dispatch = useDispatch();

  useEffect(() => {
    // clear selections list
    organizationUIProps.setIds([]);

    // server call by queryParams
    dispatch(actions.fetchOrganizationList(organizationUIProps.queryParams));

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [organizationUIProps.queryParams, dispatch]);

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
    },
    {
      dataField: "name",
      text: "Name",
    },
    {
      dataField: "country",
      text: "Country",
    },
    {
      dataField: "organization_subscriptions",
      text: "Subscription Type",
    },
    {
      dataField: "active",
      text: "Status",
      formatter: columnFormatters.StatusColumnFormatter,
    },
    {
      dataField: "organization_user",
      text: "#Users",
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditOrganizationPage: organizationUIProps.openEditOrganizationPage,
        openDeleteOrganizationDialog:
          organizationUIProps.openDeleteOrganizationDialog,
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
                organizationUIProps.setQueryParams
              )}
              selectRow={getSelectRow({
                entities,
                ids: organizationUIProps.ids,
                setIds: organizationUIProps.setIds,
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
