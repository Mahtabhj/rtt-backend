import React from "react";
import { Route } from "react-router-dom";
import { DocumentLoadingDialog } from "./document-loading-dialog/DocumentLoadingDialog";
import { DocumentDeleteDialog } from "./document-delete-dialog/DocumentDeleteDialog";
import { DocumentCard } from "./DocumentCard";
import { DocumentUIProvider } from "./DocumentUIContext";

export function DocumentPage({ history }) {
  const documentUIEvents = {
    newDocumentButtonClick: () => {
      history.push("/backend/document-info/documents/new");
    },
    openEditDocumentPage: (id) => {
      history.push(`/backend/document-info/documents/${id}/edit`);
    },
    openSelectDocumentPage: (id) => {
      history.push(`/backend/document-info/documents/${id}/select`);
    },
    openDeleteDocumentDialog: (id) => {
      history.push(`/backend/document-info/documents/${id}/delete`);
    },
    openFetchDocumentDialog: () => {
      history.push(`/backend/document-info/documents/fetch`);
    },
    openUpdateDocumentStatusDialog: () => {
      history.push("/backend/document-info/documents/updateStatus");
    },
  };

  return (
    <DocumentUIProvider documentUIEvents={documentUIEvents}>
      <DocumentLoadingDialog />

      <Route path="/backend/document-info/documents/deleteDocument">
        {({ history, match }) => (
          <DocumentDeleteDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/document-info/documents");
            }}
          />
        )}
      </Route>

      <Route path="/backend/document-info/documents/:id/delete">
        {({ history, match }) => (
          <DocumentDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/document-info/documents");
            }}
          />
        )}
      </Route>
      <DocumentCard />
    </DocumentUIProvider>
  );
}
