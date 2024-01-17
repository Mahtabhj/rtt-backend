import React from "react";
import { Route } from "react-router-dom";
import { NewsLoadingDialog } from "./news-loading-dialog/NewsLoadingDialog";
import { NewsDeleteDialog } from "./news-delete-dialog/NewsDeleteDialog";
import { NewsFetchDialog } from "./news-fetch-dialog/NewsFetchDialog";
import { NewsUpdateStatusDialog } from "./news-update-status-dialog/NewsUpdateStatusDialog";
import { NewsCard } from "./NewsCard";
import { NewsUIProvider } from "./NewsUIContext";

export function NewsPage({ history }) {
  const newsUIEvents = {
    newNewsButtonClick: () => {
      history.push("/backend/news-info/news/new");
    },
    openEditNewsPage: (id) => {
      history.push(`/backend/news-info/news/${id}/edit`);
    },
    openSelectNewsPage: (id) => {
      history.push(`/backend/news-info/news/${id}/select`);
    },
    openDeleteNewsDialog: (id) => {
      history.push(`/backend/news-info/news/${id}/delete`);
    },
    openFetchNewsDialog: () => {
      history.push(`/backend/news-info/news/fetch`);
    },
    openUpdateNewsStatusDialog: () => {
      history.push("/backend/news-info/news/updateStatus");
    },
  };

  return (
    <NewsUIProvider newsUIEvents={newsUIEvents}>
      <NewsLoadingDialog />

      <Route path="/backend/news-info/news/deleteNews">
        {({ history, match }) => (
          <NewsDeleteDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/news-info/news");
            }}
          />
        )}
      </Route>

      <Route path="/backend/news-info/news/:id/delete">
        {({ history, match }) => (
          <NewsDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/news-info/news");
            }}
          />
        )}
      </Route>

      <Route path="/backend/news-info/news/fetch">
        {({ history, match }) => (
          <NewsFetchDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/news-info/news");
            }}
          />
        )}
      </Route>

      <Route path="/backend/news-info/news/updateStatus">
        {({ history, match }) => (
          <NewsUpdateStatusDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/news-info/news");
            }}
          />
        )}
      </Route>

      <NewsCard />
    </NewsUIProvider>
  );
}
