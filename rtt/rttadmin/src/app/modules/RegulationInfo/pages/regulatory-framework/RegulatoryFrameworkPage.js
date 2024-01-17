import React from "react";
import { Route } from "react-router-dom";
import { RegulatoryFrameworkLoadingDialog } from "./regulatory-framework-loading-dialog/RegulatoryFrameworkLoadingDialog";
import { RegulatoryFrameworkDeleteDialog } from "./regulatory-framework-delete-dialog/RegulatoryFrameworkDeleteDialog";
import { RegulatoryFrameworkCard } from "./RegulatoryFrameworkCard";
import { RegulatoryFrameworkUIProvider } from "./RegulatoryFrameworkUIContext";

export function RegulatoryFrameworkPage({ history }) {
  const regulatoryFrameworkUIEvents = {
    newRegulatoryFrameworkButtonClick: () => {
      history.push("/backend/regulation-info/regulatory-framework/new");
    },
    openEditRegulatoryFrameworkPage: (id) => {
      history.push(`/backend/regulation-info/regulatory-framework/${id}/edit`);
    },
    openSelectRegulatoryFrameworkPage: (id) => {
      history.push(
        `/backend/regulation-info/regulatory-framework/${id}/select`
      );
    },
    openDeleteRegulatoryFrameworkDialog: (id) => {
      history.push(
        `/backend/regulation-info/regulatory-framework/${id}/delete`
      );
    },
  };
  
  return (
    <RegulatoryFrameworkUIProvider
      regulatoryFrameworkUIEvents={regulatoryFrameworkUIEvents}
    >
      <RegulatoryFrameworkLoadingDialog />

      <Route path="/backend/regulation-info/regulatory-framework/:id/delete">
        {({ history, match }) => (
          <RegulatoryFrameworkDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/regulation-info/regulatory-framework");
            }}
          />
        )}
      </Route>
      <RegulatoryFrameworkCard />
    </RegulatoryFrameworkUIProvider>
  );
}
