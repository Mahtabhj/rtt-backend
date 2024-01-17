import React from "react";
import { Route } from "react-router-dom";
import { RegulationLoadingDialog } from "./regulation-loading-dialog/RegulationLoadingDialog";
import { RegulationDeleteDialog } from "./regulation-delete-dialog/RegulationDeleteDialog";
import { RegulationCard } from "./RegulationCard";
import { RegulationUIProvider } from "./RegulationUIContext";

export function RegulationPage({ history }) {
  const regulationUIEvents = {
    newRegulationButtonClick: () => {
      history.push("/backend/regulation-info/regulation/new");
    },
    openEditRegulationPage: (id) => {
      history.push(`/backend/regulation-info/regulation/${id}/edit`);
    },
    openSelectRegulationPage: (id) => {
      history.push(`/backend/regulation-info/regulation/${id}/select`);
    },
    openDeleteRegulationDialog: (id) => {
      history.push(`/backend/regulation-info/regulation/${id}/delete`);
    },
    openFetchRegulationDialog: () => {
      history.push(`/backend/regulation-info/regulation/fetch`);
    },
    openUpdateRegulationStatusDialog: () => {
      history.push("/backend/regulation-info/regulation/updateStatus");
    },
  };

  return (
    <RegulationUIProvider regulationUIEvents={regulationUIEvents}>
      <RegulationLoadingDialog />

      <Route path="/backend/regulation-info/regulation/deleteRegulation">
        {({ history, match }) => (
          <RegulationDeleteDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/regulation-info/regulation");
            }}
          />
        )}
      </Route>

      <Route path="/backend/regulation-info/regulation/:id/delete">
        {({ history, match }) => (
          <RegulationDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/regulation-info/regulation");
            }}
          />
        )}
      </Route>

      <RegulationCard />
    </RegulationUIProvider>
  );
}
