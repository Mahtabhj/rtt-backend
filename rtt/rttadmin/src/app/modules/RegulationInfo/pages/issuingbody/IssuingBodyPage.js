import React from "react";
import { Route } from "react-router-dom";
import { IssuingBodyLoadingDialog } from "./issuingbody-loading-dialog/IssuingBodyLoadingDialog";
import { IssuingBodyDeleteDialog } from "./issuingbody-delete-dialog/IssuingBodyDeleteDialog";
import { IssuingBodyCard } from "./IssuingBodyCard";
import { IssuingBodyUIProvider } from "./IssuingBodyUIContext";

export function IssuingBodyPage({ history }) {
  const issuingbodyUIEvents = {
    newIssuingBodyButtonClick: () => {
      history.push("/backend/regulation-info/issuingbody/new");
    },
    openEditIssuingBodyPage: (id) => {
      history.push(`/backend/regulation-info/issuingbody/${id}/edit`);
    },
    openSelectIssuingBodyPage: (id) => {
      history.push(`/backend/regulation-info/issuingbody/${id}/select`);
    },
    openDeleteIssuingBodyDialog: (id) => {
      history.push(`/backend/regulation-info/issuingbody/${id}/delete`);
    },
    openFetchIssuingBodyDialog: () => {
      history.push(`/backend/regulation-info/issuingbody/fetch`);
    },
    openUpdateIssuingBodyStatusDialog: () => {
      history.push("/backend/regulation-info/issuingbody/updateStatus");
    },
  };

  return (
    <IssuingBodyUIProvider issuingbodyUIEvents={issuingbodyUIEvents}>
      <IssuingBodyLoadingDialog />

      <Route path="/backend/regulation-info/issuingbody/:id/delete">
        {({ history, match }) => (
          <IssuingBodyDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/regulation-info/issuingbody");
            }}
          />
        )}
      </Route>

      <IssuingBodyCard />
    </IssuingBodyUIProvider>
  );
}
