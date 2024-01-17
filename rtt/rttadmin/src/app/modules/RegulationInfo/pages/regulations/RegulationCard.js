import React, { useEffect, useMemo } from "react";
import { useDispatch, useSelector } from "react-redux";

import { updateSearchValue } from "@redux-regulation/regulation/regulationSlice";
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
import { FilterModal, Search } from "@common";
import { RegulationTable } from "./regulation-table/RegulationTable";
import { useRegulationUIContext } from "./RegulationUIContext";

export function RegulationCard() {
  const dispatch = useDispatch();
  const regulationUIContext = useRegulationUIContext();
  const regulationUIProps = useMemo(() => {
    return {
      ids: regulationUIContext.ids,
      queryParams: regulationUIContext.queryParams,
      setQueryParams: regulationUIContext.setQueryParams,
      newRegulationButtonClick: regulationUIContext.newRegulationButtonClick,
      openDeleteRegulationsDialog: regulationUIContext.openDeleteRegulationsDialog,
      openEditRegulationPage: regulationUIContext.openEditRegulationPage,
      openSelectRegulationPage: regulationUIContext.openSelectRegulationPage,
      openUpdateRegulationStatusDialog: regulationUIContext.openUpdateRegulationStatusDialog,
      openFetchRegulationDialog: regulationUIContext.openFetchRegulationDialog,
    };
  }, [regulationUIContext]);

  const { filterOptions, isFiltered, searchValue } = useSelector(
    (state) => ({
      filterOptions: state.regulation.filterOptions,
      isFiltered: state.regulation.isFiltered,
      searchValue: state.regulation.searchValue,
    })
  );

  const filterQueryParams = useMemo(() => prepareFilterQueryParams(filterOptions), [filterOptions]);

  useEffect(() => {
    const currentQueryParams = regulationUIProps.queryParams;

    const filterWithSearchQueryParams = { ...filterQueryParams, search: searchValue || null };
    // may need to check currentQueryParams for fields sortField & sortOrder
    const checkForUpdateQueryParams =
      isCurrentQueryParamsNotContainFilterQueryParams(currentQueryParams, filterWithSearchQueryParams);

    checkForUpdateQueryParams
    &&
    regulationUIProps.setQueryParams({
      ...regulationUIProps.queryParams,
      ...filterQueryParams,
      search: searchValue || null
    });
  }, [isFiltered, filterQueryParams, searchValue]);

  const handleUpdateSearchValue = (value) => {
    dispatch(updateSearchValue(value));
  }

  return (
    <Card>
      <CardHeader title="Regulation List">
        <CardHeaderToolbar>
          <button
            type="button"
            className="btn btn-primary"
            onClick={regulationUIProps.newRegulationButtonClick}
          >
            Create Regulation
          </button>
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        <div className="d-flex justify-content-between flex-wrap mb-5">
          <div className="form-group">
            <Search handleUpdateSearch={handleUpdateSearchValue} initialValue={searchValue} />
          </div>
          <div className="popup">
            <FilterModal filterType={'regulation'} />
          </div>
        </div>

        <RegulationTable />
      </CardBody>
    </Card>
  );
}
