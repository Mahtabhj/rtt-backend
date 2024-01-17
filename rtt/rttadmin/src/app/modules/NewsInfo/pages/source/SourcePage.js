import React from "react";
import { Route } from "react-router-dom";
import { SourceLoadingDialog } from "./source-loading-dialog/SourceLoadingDialog";
import { SourceDeleteDialog } from "./source-delete-dialog/SourceDeleteDialog";
import { SourceFetchDialog } from "./source-fetch-dialog/SourceFetchDialog";
import { SourceUpdateStatusDialog } from "./source-update-status-dialog/SourceUpdateStatusDialog";
import { SourceCard } from "./SourceCard";
import { SourceUIProvider } from "./SourceUIContext";

export function SourcePage({ history }) {
  const sourceUIEvents = {
    newSourceButtonClick: () => {
      history.push("/backend/news-info/sources/new");
    },
    openEditSourcePage: (id) => {
      history.push(`/backend/news-info/sources/${id}/edit`);
    },
    openSelectSourcePage: (id) => {
      history.push(`/backend/news-info/sources/${id}/select`);
    },
    openDeleteSourceDialog: (id) => {
      history.push(`/backend/news-info/sources/${id}/delete`);
    },
    openFetchSourceDialog: () => {
      history.push(`/backend/news-info/sources/fetch`);
    },
    openUpdateSourceStatusDialog: () => {
      history.push("/backend/news-info/sources/updateStatus");
    },
  };

  return (
    <SourceUIProvider sourceUIEvents={sourceUIEvents}>
      <SourceLoadingDialog />

      <Route path="/backend/news-info/sources/deleteSource">
        {({ history, match }) => (
          <SourceDeleteDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/news-info/sources");
            }}
          />
        )}
      </Route>

      <Route path="/backend/news-info/sources/:id/delete">
        {({ history, match }) => (
          <SourceDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/news-info/sources");
            }}
          />
        )}
      </Route>

      <Route path="/backend/news-info/sources/fetch">
        {({ history, match }) => (
          <SourceFetchDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/news-info/sources");
            }}
          />
        )}
      </Route>

      <Route path="/backend/news-info/source/updateStatus">
        {({ history, match }) => (
          <SourceUpdateStatusDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/news-info/sources");
            }}
          />
        )}
      </Route>

      <SourceCard />
    </SourceUIProvider>
  );
}
