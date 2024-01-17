import React from "react";
import { Route, useHistory } from "react-router-dom";
import { OrganizationLoadingDialog } from "./organization-loading-dialog/OrganizationLoadingDialog";
import { OrganizationDeleteDialog } from "./organization-delete-dialog/OrganizationDeleteDialog";
import { OrganizationFetchDialog } from "./organization-fetch-dialog/OrganizationFetchDialog";
import { OrganizationCard } from "./OrganizationCard";
import { OrganizationUIProvider } from "./OrganizationUIContext";

export function OrganizationPage() {
  const history = useHistory();

  const organizationUIEvents = {
    newOrganizationButtonClick: () => {
      history.push("/backend/organization-info/organizations/new");
    },
    openEditOrganizationPage: (id) => {
      history.push(`/backend/organization-info/organizations/${id}/edit`);
    },
    openSelectOrganizationPage: (id) => {
      history.push(`/backend/organization-info/organizations/${id}/select`);
    },
    openDeleteOrganizationDialog: (id) => {
      history.push(`/backend/organization-info/organizations/${id}/delete`);
    },
    openFetchOrganizationDialog: () => {
      history.push(`/backend/organization-info/organizations/fetch`);
    },
    openUpdateOrganizationStatusDialog: () => {
      history.push("/backend/organization-info/organizations/updateStatus");
    },
  };

  return (
    <OrganizationUIProvider organizationUIEvents={organizationUIEvents}>
      <OrganizationLoadingDialog />

      <Route path="/backend/organization-info/organizations/deleteOrganization">
        {({ history, match }) => (
          <OrganizationDeleteDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/organization-info/organizations");
            }}
          />
        )}
      </Route>

      <Route path="/backend/organization-info/organizations/:id/delete">
        {({ history, match }) => (
          <OrganizationDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/organization-info/organizations");
            }}
          />
        )}
      </Route>

      <Route path="/backend/organization-info/organizations/fetch">
        {({ history, match }) => (
          <OrganizationFetchDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/organization-info/organizations");
            }}
          />
        )}
      </Route>

      <OrganizationCard />

    </OrganizationUIProvider>
  );
}
