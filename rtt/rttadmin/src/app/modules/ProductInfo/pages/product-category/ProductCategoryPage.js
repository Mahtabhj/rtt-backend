import React from "react";
import { Route } from "react-router-dom";
import { ProductCategoryLoadingDialog } from "./product-category-loading-dialog/ProductCategoryLoadingDialog";
import { ProductCategoryDeleteDialog } from "./product-category-delete-dialog/ProductCategoryDeleteDialog";
import { ProductCategoryCard } from "./ProductCategoryCard";
import { ProductCategoryUIProvider } from "./ProductCategoryUIContext";

export function ProductCategoryPage({ history }) {
  const productCategoryUIEvents = {
    newProductCategoryButtonClick: () => {
      history.push("/backend/product-info/product-categories/new");
    },
    openEditProductCategoryPage: (id) => {
      history.push(`/backend/product-info/product-categories/${id}/edit`);
    },
    openDeleteProductCategoryDialog: (id) => {
      history.push(`/backend/product-info/product-categories/${id}/delete`);
    },
    openFetchProductCategoryDialog: () => {
      history.push(`/backend/product-info/product-categories/fetch`);
    },
    openUpdateProductCategoryStatusDialog: () => {
      history.push("/backend/product-info/product-categories/updateStatus");
    },
  };

  return (
    <ProductCategoryUIProvider
      productCategoryUIEvents={productCategoryUIEvents}
    >
      <ProductCategoryLoadingDialog />

      <Route path="/backend/product-info/product-categories/deleteProductCategory">
        {({ history, match }) => (
          <ProductCategoryDeleteDialog
            show={match != null}
            onHide={() => {
              history.push("/backend/product-info/product-categories");
            }}
          />
        )}
      </Route>

      <Route path="/backend/product-info/product-categories/:id/delete">
        {({ history, match }) => (
          <ProductCategoryDeleteDialog
            show={match != null}
            id={match && match.params.id}
            onHide={() => {
              history.push("/backend/product-info/product-categories");
            }}
          />
        )}
      </Route>

      <ProductCategoryCard />
    </ProductCategoryUIProvider>
  );
}
