import React from "react";
import { Route } from "react-router-dom";
import { MaterialCategoryLoadingDialog } from "./material-category-loading-dialog/MaterialCategoryLoadingDialog";
import { MaterialCategoryDeleteDialog } from "./material-category-delete-dialog/MaterialCategoryDeleteDialog";
import { MaterialCategoryCard } from "./MaterialCategoryCard";
import { MaterialCategoryUIProvider } from "./MaterialCategoryUIContext";

export function MaterialCategoryPage({ history }) {
  const materialCategoryUIEvents = {
    newMaterialCategoryButtonClick: () => {
      history.push("/backend/product-info/material-categories/new");
    },
    openEditMaterialCategoryPage: (id) => {
      history.push(`/backend/product-info/material-categories/${id}/edit`);
    },
    openDeleteMaterialCategoryDialog: (id) => {
      history.push(`/backend/product-info/material-categories/${id}/delete`);
    },
    openFetchMaterialCategoryDialog: () => {
      history.push(`/backend/product-info/material-categories/fetch`);
    },
    openUpdateMaterialCategoryStatusDialog: () => {
      history.push("/backend/product-info/material-categories/updateStatus");
    },
  };

  return (
    <MaterialCategoryUIProvider
      materialCategoryUIEvents={materialCategoryUIEvents}
    >
      <MaterialCategoryLoadingDialog />

      <Route path="/backend/product-info/material-categories/deleteMaterialCategory">
        {({ history, match }) => (
          <MaterialCategoryDeleteDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/product-info/material-categories");
            }}
          />
        )}
      </Route>

      <Route path="/backend/product-info/material-categories/:id/delete">
        {({ history, match }) => (
          <MaterialCategoryDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/product-info/material-categories");
            }}
          />
        )}
      </Route>

      <MaterialCategoryCard />
    </MaterialCategoryUIProvider>
  );
}
