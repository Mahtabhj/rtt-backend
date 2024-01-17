import React, { useEffect, useState } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import * as actions from "@redux-organization/organization/organizationActions";
import * as uiHelpers from "../../users/UsersUIHelpers";
import {
  NoRecordsFoundMessage,
  PleaseWaitMessage,
  pageListRenderer,
} from "@metronic-helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";

import { UserAddEditModal } from "./UserAddEditModal";
import { UserDeleteDialog } from "./UserDeleteDialog";
import { UserPasswordChangeModal } from "./UserPasswordChangeModal";

import * as columnFormatters from "./column-formatters";

export function UsersTable({ history, organizationId }) {
  // Organization UI Context

  // Getting curret state of organization users list from store (Redux)
  const { currentState } = useSelector(
    (state) => ({ currentState: state.organization }),
    shallowEqual
  );

  const { users, totalCount } = currentState;

  // Organization Redux state
  const dispatch = useDispatch();

  const [showUserAddModal, setShowUserAddModal] = useState(false);
  const [showUserDeleteModal, setShowUserDeleteModal] = useState(false);
  const [
    showUserPasswordChangeModal,
    setShowUserPasswordChangeModal,
  ] = useState(false);

  const [selectedUserId, setSelectedUserId] = useState(null);
  const [selectedUserIdDelete, setSelectedUserIdDelete] = useState(null);

  useEffect(() => {
    // server call by queryParams
    dispatch(actions.fetchOrganizationUserList(organizationId));

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
      dataField: "first_name",
      text: "First Name",
      sort: true,
    },
    {
      dataField: "last_name",
      text: "Last Name",
      sort: true,
    },
    {
      dataField: "email",
      text: "Email",
      sort: true,
    },
    {
      dataField: "city",
      text: "City",
      sort: true,
    },
    {
      dataField: "country",
      text: "Country",
      sort: true,
    },

    {
      dataField: "is_active",
      text: "Status",
      formatter: columnFormatters.StatusColumnFormatter,
    },
    {
      dataField: "is_admin",
      text: "Role",
      formatter: columnFormatters.AdminColumnFormatter,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openPasswordChangeDialog: (id) => {
          setSelectedUserId(id);
          setShowUserPasswordChangeModal(true);
        },
        openEditOrganizationUserPage: (id) => {
          setShowUserAddModal(true);
          setSelectedUserId(id);
        },
        openDeleteOrganizationUserDialog: (id) => {
          setSelectedUserIdDelete(id);
          setShowUserDeleteModal(true);
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
    totalSize: totalCount,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <Card>
        <CardHeader title="Users list">
          <CardHeaderToolbar>
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => {
                setSelectedUserId(null);
                setShowUserAddModal(true);
              }}
            >
              New User
            </button>
          </CardHeaderToolbar>
        </CardHeader>

        <PaginationProvider pagination={paginationFactory(paginationOptions)}>
          {({ paginationProps, paginationTableProps }) => {
            return (
              <BootstrapTable
                wrapperClasses="table-responsive"
                classes="table table-head-custom table-vertical-center overflow-hidden"
                bootstrap4
                bordered={false}
                keyField="id"
                data={users === null ? [] : users}
                columns={columns}
                defaultSorted={uiHelpers.defaultSorted}
                onTableChange={() => null}
                {...paginationTableProps}
              >
                <PleaseWaitMessage entities={users} />
                <NoRecordsFoundMessage entities={users} />
              </BootstrapTable>
            );
          }}
        </PaginationProvider>
      </Card>
      <UserAddEditModal
        organizationId={organizationId}
        selectedUserId={selectedUserId}
        showUserAddModal={showUserAddModal}
        setShowUserAddModal={setShowUserAddModal}
      />
      <UserPasswordChangeModal
        selectedUserId={selectedUserId}
        showUserPasswordChangeModal={showUserPasswordChangeModal}
        setShowUserPasswordChangeModal={setShowUserPasswordChangeModal}
      />

      <UserDeleteDialog
        organizationId={organizationId}
        selectedUserIdDelete={selectedUserIdDelete}
        showUserDeleteModal={showUserDeleteModal}
        setShowUserDeleteModal={setShowUserDeleteModal}
      />
    </>
  );
}
