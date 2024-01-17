import React, { useEffect, useMemo } from "react";
import { useDispatch, useSelector } from "react-redux";

import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import {
  isCurrentQueryParamsNotContainFilterQueryParams,
  prepareFilterQueryParams
} from "@metronic-helpers";
import { updateSearchValue } from "@redux-regulation/regulatory-framework/regulatoryFrameworkSlice";
import { fetchStatusList } from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import {
  fetchIssuingBodyList,
  fetchRegionList,
} from "@redux-regulation/issuingbody/issuingbodyActions";
import { fetchMaterialCategoryList } from "@redux-product/material-category/materialCategoryActions";
import { fetchProductCategoryList } from "@redux-product/product-category/productCategoryActions";
import { RegulatoryFrameworkTable } from "./regulatory-framework-table/RegulatoryFrameworkTable";
import { useRegulatoryFrameworkUIContext } from "./RegulatoryFrameworkUIContext";
import { FilterModal, Search } from "@common";

export function RegulatoryFrameworkCard() {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchIssuingBodyList());
    dispatch(fetchStatusList());
    dispatch(fetchRegionList());
    dispatch(fetchMaterialCategoryList());
    dispatch(fetchProductCategoryList());
  }, [dispatch]);

  const regulatoryFrameworkUIContext = useRegulatoryFrameworkUIContext();
  const regulatoryFrameworkUIProps = useMemo(() => {
    return {
      ids: regulatoryFrameworkUIContext.ids,
      queryParams: regulatoryFrameworkUIContext.queryParams,
      setQueryParams: regulatoryFrameworkUIContext.setQueryParams,
      newRegulatoryFrameworkButtonClick:
        regulatoryFrameworkUIContext.newRegulatoryFrameworkButtonClick,
      openDeleteRegulatoryFrameworksDialog:
        regulatoryFrameworkUIContext.openDeleteRegulatoryFrameworksDialog,
      openEditRegulatoryFrameworkPage:
        regulatoryFrameworkUIContext.openEditRegulatoryFrameworkPage,
      openSelectRegulatoryFrameworkPage:
        regulatoryFrameworkUIContext.openSelectRegulatoryFrameworkPage,
      openUpdateRegulatoryFrameworkStatusDialog:
        regulatoryFrameworkUIContext.openUpdateRegulatoryFrameworkStatusDialog,
      openFetchRegulatoryFrameworkDialog:
        regulatoryFrameworkUIContext.openFetchRegulatoryFrameworkDialog,
    };
  }, [regulatoryFrameworkUIContext]);

  const { filterOptions, isFiltered, searchValue } = useSelector(
    (state) => ({
      filterOptions: state.regulatoryFramework.filterOptions,
      isFiltered: state.regulatoryFramework.isFiltered,
      searchValue: state.regulatoryFramework.searchValue,
    })
  );

  const filterQueryParams = useMemo(() => prepareFilterQueryParams(filterOptions), [filterOptions]);

  useEffect(() => {
    const currentQueryParams = regulatoryFrameworkUIProps.queryParams;

    const filterWithSearchQueryParams = { ...filterQueryParams, search: searchValue || null };
    const checkForUpdateQueryParams =
      isCurrentQueryParamsNotContainFilterQueryParams(currentQueryParams, filterWithSearchQueryParams);

    checkForUpdateQueryParams
    &&
    regulatoryFrameworkUIProps.setQueryParams({
      ...regulatoryFrameworkUIProps.queryParams,
      ...filterQueryParams,
      search: searchValue || null
    });
  }, [isFiltered, filterQueryParams, searchValue]);

  const handleUpdateSearchValue = (value) => {
    dispatch(updateSearchValue(value));
  }

  return (
    <Card>
      <CardHeader title="Regulatory Framework List">
        <CardHeaderToolbar>
          <button
            type="button"
            className="btn btn-primary"
            onClick={regulatoryFrameworkUIProps.newRegulatoryFrameworkButtonClick}
          >
            Create Regulatory Framework
          </button>
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        <div className="d-flex justify-content-between flex-wrap">
          <div className="form-group">
            <Search handleUpdateSearch={handleUpdateSearchValue} initialValue={searchValue} />
          </div>
          <div className="popup">
            <FilterModal filterType={'regulatoryFramework'} />
          </div>
        </div>

        <RegulatoryFrameworkTable />
      </CardBody>
    </Card>
  );
}
