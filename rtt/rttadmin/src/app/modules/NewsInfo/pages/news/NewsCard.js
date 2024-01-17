import React, { useCallback, useEffect, useMemo, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import * as actions from "@redux-news/news/newsActions";
import { setTab, resetFilter, updateSearchValue } from "@redux-news/news/newsSlice";

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

import { ImportModal, FilterModal, Search } from "@common";

import { NewsTable } from "./news-table/NewsTable";
import { useNewsUIContext } from "./NewsUIContext";
import { initialFilter } from "./NewsUIHelpers";
import { TAB, tabFilterOption } from "./constants";


export function NewsCard() {
  const dispatch = useDispatch();
  const newsUIContext = useNewsUIContext();
  const newsUIProps = useMemo(() => {
    return {
      ids: newsUIContext.ids,
      queryParams: newsUIContext.queryParams,
      setQueryParams: newsUIContext.setQueryParams,
      newNewsButtonClick: newsUIContext.newNewsButtonClick,
      openDeleteNewsDialog: newsUIContext.openDeleteNewsDialog,
      openEditNewsPage: newsUIContext.openEditNewsPage,
      openSelectNewsPage: newsUIContext.openSelectNewsPage,
      openUpdateNewsStatusDialog: newsUIContext.openUpdateNewsStatusDialog,
      openFetchNewsDialog: newsUIContext.openFetchNewsDialog,
    };
  }, [newsUIContext]);

  const {
    tab,
    filterOptions,
    isFiltered,
    searchValue,
    reviewCount,
    totalCount,
    actionsLoading,
  } = useSelector(
    ({ news }) => ({
      tab: news.tab,
      filterOptions: news.filterOptions,
      isFiltered: news.isFiltered,
      searchValue: news.searchValue,
      reviewCount: news.reviewCount,
      totalCount: news.totalCount,
      actionsLoading: news.actionsLoading,
    })
  );

  useEffect(() => {
    dispatch(actions.fetchRegionList());
    dispatch(actions.fetchCategoryList());
    dispatch(actions.fetchProductCategoryList());
  }, [dispatch]);

  const filterQueryParams = useMemo(() => prepareFilterQueryParams(filterOptions), [filterOptions]);

  useEffect(() => {
    const currentQueryParams = newsUIProps.queryParams;

    if (currentQueryParams.runQuery) {
      const filterWithSearchQueryParams = { ...filterQueryParams, search: searchValue || null };
      const checkForUpdateQueryParams =
        isCurrentQueryParamsNotContainFilterQueryParams(currentQueryParams, filterWithSearchQueryParams);

      if (checkForUpdateQueryParams) {
        newsUIProps.setQueryParams({
          ...newsUIProps.queryParams,
          ...filterQueryParams,
          search: searchValue || null,
          runQuery: true
        });
      }
    } else {
      newsUIProps.setQueryParams({
        ...initialFilter,
        ...tabFilterOption[tab],
        ...filterQueryParams,
        search: searchValue || null,
        runQuery: true,
      });
    }
  }, [isFiltered, filterQueryParams, searchValue, tab]);

  const handleUpdateSearchValue = useCallback(value => dispatch(updateSearchValue(value)), [dispatch]);

  const handleChangeTab = e => {
    const newTab = e.currentTarget.id;

    if (newTab !== tab) {
      dispatch(updateSearchValue(''));
      dispatch(resetFilter());
      dispatch(setTab(newTab));

      newsUIProps.setQueryParams({
        ...initialFilter,
        ...tabFilterOption[newTab],
        runQuery: true,
      });
    }
  };

  const actionImportNews = actions.saveNewsFromDate;

  const getOpenReviewTabCount = () => {
    // if review tab selected use min count (BE not implement filtering for the review_count)
    if (tab === TAB.REVIEW) return totalCount < reviewCount ? totalCount : reviewCount;

    return reviewCount;
  };

  return (
    <Card>
      <CardHeader title="News list">
        <CardHeaderToolbar>
          <ImportModal
            title="News"
            actionImport={actionImportNews}
            actionsLoading={actionsLoading}
          />
          <button
            type="button"
            className="btn btn-primary ml-3"
            onClick={newsUIProps.newNewsButtonClick}
          >
            Create News
          </button>
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        <div className="d-flex justify-content-between flex-wrap">
          <div className="form-group">
            <Search handleUpdateSearch={handleUpdateSearchValue} initialValue={searchValue} />
          </div>
          <div className="popup">
            <FilterModal filterType={'news'}/>
          </div>
        </div>
        <ul className="nav nav-tabs nav-tabs-line " role="tablist">
          <li className="nav-item" id={TAB.NEW} onClick={handleChangeTab}>
            <a
              name={TAB.NEW}
              className={`nav-link ${tab === TAB.NEW && "active"}`}
              data-toggle="tab"
              role="tab"
              aria-selected={(tab === TAB.NEW).toString()}
              href="#/"
            >
              To be processed
            </a>
          </li>

          <li className="nav-item" id={TAB.SELECTED} onClick={handleChangeTab}>
            <a
              name={TAB.SELECTED}
              className={`nav-link ${tab === TAB.SELECTED && "active"}`}
              data-toggle="tab"
              role="tab"
              aria-selected={(tab === TAB.SELECTED).toString()}
              href="#/"
            >
              Draft
            </a>
          </li>

          <li className="nav-item" id={TAB.ONLINE} onClick={handleChangeTab}>
            <a
              name={TAB.ONLINE}
              className={`nav-link ${tab === TAB.ONLINE && "active"}`}
              data-toggle="tab"
              role="tab"
              aria-selected={(tab === TAB.ONLINE).toString()}
              href="#/"
            >
              Online
            </a>
          </li>

          <li className="nav-item" id={TAB.DISCHARGED} onClick={handleChangeTab}>
            <a
              name={TAB.DISCHARGED}
              className={`nav-link ${tab === TAB.DISCHARGED && "active"}`}
              data-toggle="tab"
              role="tab"
              aria-selected={(tab === TAB.DISCHARGED).toString()}
              href="#/"
            >
              Discharged
            </a>
          </li>

          <li className="nav-item" id={TAB.REVIEW} onClick={handleChangeTab}>
            <a
              name={TAB.REVIEW}
              className={`nav-link ${tab === TAB.REVIEW && "active"}`}
              data-toggle="tab"
              role="tab"
              aria-selected={(tab === TAB.REVIEW).toString()}
              href="#/"
            >
              Open review ({ getOpenReviewTabCount() })
            </a>
          </li>
        </ul>

        <div className="mt-5">
          <NewsTable selectedTab={tab} />
        </div>
      </CardBody>
    </Card>
  );
}
