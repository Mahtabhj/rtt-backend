import React, { useEffect, useState } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import * as actions from "@redux-organization/organization/organizationActions";
import * as uiHelpers from "./SubscriptionUIHelpers";
import {
  NoRecordsFoundMessage,
  PleaseWaitMessage,
} from "@metronic-helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";

import { SubscriptionAddEditModal } from "./SubscriptionAddEditModal";
import { SubscriptionDeleteDialog } from "./SubscriptionDeleteDialog";

import * as columnFormatters from "./column-formatters";

export function SubscriptionsTable({ history, organizationId }) {
  // Organization UI Context

  // Getting curret state of organization subscriptions list from store (Redux)
  const { currentState } = useSelector(
    (state) => ({ currentState: state.organization }),
    shallowEqual
  );

  const {
    subscriptions,
  } = currentState;

  // Organization Redux state
  const dispatch = useDispatch();

  const [showSubscriptionAddModal, setShowSubscriptionAddModal] = useState(
    false
  );
  const [
    showSubscriptionDeleteModal,
    setShowSubscriptionDeleteModal,
  ] = useState(false);

  const [selectedSubscriptionId, setSelectedSubscriptionId] = useState(null);
  const [
    selectedSubscriptionIdDelete,
    setSelectedSubscriptionIdDelete,
  ] = useState(null);

  useEffect(() => {
    // server call by queryParams
    dispatch(actions.fetchOrganizationSubscriptionList(organizationId));

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dispatch]);

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },
    {
      dataField: "type",
      text: "Type",
      sort: true,
    },
    {
      dataField: "start_date",
      text: "Start Date",
      sort: true,
      formatter: columnFormatters.DateFormatter,
    },
    {
      dataField: "end_date",
      text: "End Date",
      sort: true,
      formatter: columnFormatters.DateFormatter,
    },
    {
      dataField: "amount",
      text: "Amount",
      sort: true,
    },
    {
      dataField: "max_user",
      text: "Max User",
      sort: true,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditOrganizationSubscriptionPage: (id) => {
          setShowSubscriptionAddModal(true);
          setSelectedSubscriptionId(id);
        },
        openDeleteOrganizationSubscriptionDialog: (id) => {
          setSelectedSubscriptionIdDelete(id);
          setShowSubscriptionDeleteModal(true);
        },
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
    custom: true,
    totalSize: 10,
    sizePerPageList: uiHelpers.sizePerPageList,
    sizePerPage: 3,
    page: 1,
  };

  return (
    <>
      <Card>
        <CardHeader title="Subscriptions list">
          <CardHeaderToolbar>
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => {
                setSelectedSubscriptionId(null);
                setShowSubscriptionAddModal(true);
              }}
            >
              New Subscription
            </button>
          </CardHeaderToolbar>
        </CardHeader>

        <PaginationProvider pagination={paginationFactory(paginationOptions)}>
          {({ paginationProps, paginationTableProps }) => {
            return (
              // <Pagination
              //   isLoading={listLoading}
              //   paginationProps={paginationProps}
              // >
              <BootstrapTable
                wrapperClasses="table-responsive"
                classes="table table-head-custom table-vertical-center overflow-hidden"
                bootstrap4
                bordered={false}
                remote
                keyField="id"
                data={subscriptions === null ? [] : subscriptions}
                columns={columns}
                defaultSorted={uiHelpers.defaultSorted}
                onTableChange={() => null}
                {...paginationTableProps}
              >
                <PleaseWaitMessage entities={subscriptions} />
                <NoRecordsFoundMessage entities={subscriptions} />
              </BootstrapTable>
              // </Pagination>
            );
          }}
        </PaginationProvider>
      </Card>
      <SubscriptionAddEditModal
        organizationId={organizationId}
        selectedSubscriptionId={selectedSubscriptionId}
        showSubscriptionAddModal={showSubscriptionAddModal}
        setShowSubscriptionAddModal={setShowSubscriptionAddModal}
      />

      <SubscriptionDeleteDialog
        organizationId={organizationId}
        selectedSubscriptionIdDelete={selectedSubscriptionIdDelete}
        showSubscriptionDeleteModal={showSubscriptionDeleteModal}
        setShowSubscriptionDeleteModal={setShowSubscriptionDeleteModal}
      />
    </>
  );
}
