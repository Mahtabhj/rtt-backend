import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./ProductCategoryUIHelpers";

const ProductCategoryUIContext = createContext();

export function useProductCategoryUIContext() {
  return useContext(ProductCategoryUIContext);
}

export const ProductCategoryUIConsumer = ProductCategoryUIContext.Consumer;

export function ProductCategoryUIProvider({ productCategoryUIEvents, children }) {
  const [queryParams, setQueryParamsBase] = useState(initialFilter);
  const [ids, setIds] = useState([]);

  const setQueryParams = useCallback((nextQueryParams) => {
    setQueryParamsBase((prevQueryParams) => {
      if (isFunction(nextQueryParams)) {
        nextQueryParams = nextQueryParams(prevQueryParams);
      }

      if (isEqual(prevQueryParams, nextQueryParams)) {
        return prevQueryParams;
      }

      return nextQueryParams;
    });
  }, []);


  const value = {
    queryParams,
    setQueryParamsBase,
    ids,
    setIds,
    setQueryParams,
    newProductCategoryButtonClick: productCategoryUIEvents.newProductCategoryButtonClick,
    openEditProductCategoryPage: productCategoryUIEvents.openEditProductCategoryPage,
    openDeleteProductCategoryDialog: productCategoryUIEvents.openDeleteProductCategoryDialog,
    openFetchProductCategoryDialog: productCategoryUIEvents.openFetchProductCategoryDialog,
  };

  return (
    <ProductCategoryUIContext.Provider value={value}>
      {children}
    </ProductCategoryUIContext.Provider>
  );
}
