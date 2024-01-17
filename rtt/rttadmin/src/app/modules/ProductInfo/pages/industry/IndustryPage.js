import React from "react";
import { Route } from "react-router-dom";
import { IndustryLoadingDialog } from "./industry-loading-dialog/IndustryLoadingDialog";
import { IndustryDeleteDialog } from "./industry-delete-dialog/IndustryDeleteDialog";
import { IndustryCard } from "./IndustryCard";
import { IndustryUIProvider } from "./IndustryUIContext";

export function IndustryPage({ history }) {
  const industryUIEvents = {
    newIndustryButtonClick: () => {
      history.push("/backend/product-info/industries/new");
    },
    openEditIndustryPage: (id) => {
      history.push(`/backend/product-info/industries/${id}/edit`);
    },
    openDeleteIndustryDialog: (id) => {
      history.push(`/backend/product-info/industries/${id}/delete`);
    },
    openFetchIndustryDialog: () => {
      history.push(`/backend/product-info/industries/fetch`);
    },
    openUpdateIndustryStatusDialog: () => {
      history.push("/backend/product-info/industries/updateStatus");
    },
  };

  return (
    <IndustryUIProvider industryUIEvents={industryUIEvents}>
      <IndustryLoadingDialog />

      <Route path="/backend/product-info/industries/deleteIndustry">
        {({ history, match }) => (
          <IndustryDeleteDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/product-info/industries");
            }}
          />
        )}
      </Route>

      <Route path="/backend/product-info/industries/:id/delete">
        {({ history, match }) => (
          <IndustryDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/product-info/industries");
            }}
          />
        )}
      </Route>

      <IndustryCard />
    </IndustryUIProvider>
  );
}
