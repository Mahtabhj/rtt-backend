import React from "react";
import { Route } from "react-router-dom";
import { UsersLoadingDialog } from "./users-loading-dialog/UsersLoadingDialog";
import { UserEditDialog } from "./user-edit-dialog/UserEditDialog";
import { UserDeleteDialog } from "./user-delete-dialog/UserDeleteDialog";
import { UsersFetchDialog } from "./users-fetch-dialog/UsersFetchDialog";
import { UserPasswordChangeModal } from '../organization/users-table/UserPasswordChangeModal';
import { UsersUpdateStateDialog } from "./users-update-status-dialog/UsersUpdateStateDialog";
import { UsersUIProvider } from "./UsersUIContext";
import { UsersCard } from "./UsersCard";

export function UsersPage({ history }) {
  const usersUIEvents = {
    newUserButtonClick: () => {
      history.push("/backend/organization-info/users/new");
    },
    openEditUserDialog: (id) => {
      history.push(`/backend/organization-info/users/${id}/edit`);
    },
    openDeleteUserDialog: (id) => {
      history.push(`/backend/organization-info/users/${id}/delete`);
    },
    openFetchUsersDialog: () => {
      history.push(`/backend/organization-info/users/fetch`);
    },
    openUpdateUsersStatusDialog: () => {
      history.push("/backend/organization-info/users/updateStatus");
    },
    openPasswordChangeDialog: (id) => {
      history.push(`/backend/organization-info/users/${id}/change-password`);
    }
  };

  return (
    <UsersUIProvider usersUIEvents={usersUIEvents}>
      <UsersLoadingDialog />
      <Route path="/backend/organization-info/users/new">
        {({ history, match }) => (
          <UserEditDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/organization-info/users");
            }}
          />
        )}
      </Route>
      <Route path="/backend/organization-info/users/:id/edit">
        {({ history, match }) => (
          <UserEditDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/organization-info/users");
            }}
          />
        )}
      </Route>
      <Route path="/backend/organization-info/users/:id/delete">
        {({ history, match }) => (
          <UserDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/organization-info/users");
            }}
          />
        )}
      </Route>
      <Route path="/backend/organization-info/users/fetch">
        {({ history, match }) => (
          <UsersFetchDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/organization-info/users");
            }}
          />
        )}
      </Route>
      <Route path="/backend/organization-info/users/updateStatus">
        {({ history, match }) => (
          <UsersUpdateStateDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/organization-info/users");
            }}
          />
        )}
      </Route>
      <Route path="/backend/organization-info/users/:id/change-password">
        {({ history, match }) => (
          <UserPasswordChangeModal
            selectedUserId={match && match.params.id}
            showUserPasswordChangeModal={!!match && match.params.id}
            setShowUserPasswordChangeModal={() => {
              history.push("/backend/organization-info/users");
            }}
          />
        )}
      </Route>
      <UsersCard />
    </UsersUIProvider>
  );
}
