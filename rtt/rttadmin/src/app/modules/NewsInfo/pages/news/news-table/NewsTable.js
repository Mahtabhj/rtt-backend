import React, { useEffect, useMemo } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import dayjs from "dayjs";

import { dischargeNews, fetchNewsList, updateNewsReview } from "@redux-news/news/newsActions";
import {
  getHandlerTableChange,
  NoRecordsFoundMessage,
  pageListRenderer,
  PleaseWaitMessage,
} from "@metronic-helpers";
import { NEWS, REVIEW } from "@common";
import { permissionsRoutePath } from "@common/Permissions/routesPaths";

import { useNewsUIContext } from "../NewsUIContext";
import * as uiHelpers from "../NewsUIHelpers";
import { TAB } from "../constants";

import * as columnFormatters from "./column-formatters";

export function NewsTable({ selectedTab }) {
  const history = useHistory();
  const dispatch = useDispatch();

  // News UI Context
  const newsUIContext = useNewsUIContext();
  const newsUIProps = useMemo(() => {
    return {
      ids: newsUIContext.ids,
      setIds: newsUIContext.setIds,
      queryParams: newsUIContext.queryParams,
      setQueryParams: newsUIContext.setQueryParams,
      openEditNewsPage: newsUIContext.openEditNewsPage,
      openSelectNewsPage: newsUIContext.openSelectNewsPage,
      openDeleteNewsDialog: newsUIContext.openDeleteNewsDialog,
    };
  }, [newsUIContext]);

  // Getting current state of news list from store (Redux)
  const { entities, totalCount } = useSelector(
    (state) => ({
      entities: state.news.entities,
      totalCount: state.news.totalCount,
    })
  );

  useEffect(() => {
    const queryParams = { ...newsUIProps.queryParams };

    if (queryParams.runQuery) {
      delete queryParams.runQuery;

      // server call by queryParams
      dispatch(fetchNewsList(queryParams));
    }
  }, [dispatch, newsUIProps.queryParams]);

  // Table columns
  const columns = useMemo(() => {
    const result = [];

    const commonColumns = [
      {
        dataField: "pub_date",
        text: "Date",
        formatter: (cellContent) => dayjs(cellContent).format("DD/MM/YYYY"),
      },
      {
        dataField: "title",
        text: "Title",
      },
      {
        dataField: "source",
        text: "Source",
        formatter: (cellContent) => cellContent?.name,
      },
      {
        dataField: "news_categories",
        text: "News categories",
        formatter: (cellContent) => cellContent.map(category => category?.name).join(', '),
      },
    ]

    if ([TAB.ONLINE, TAB.DISCHARGED, TAB.REVIEW].includes(selectedTab)) {
      result.push({
        dataField: "review",
        text: "Review",
        formatter: columnFormatters.ReviewColumnFormatter,
        formatExtraData: {
          handleReviewYellow: id => {
            history.push(`${permissionsRoutePath[NEWS]}/${NEWS}/${id}/edit`, { scrollTo: REVIEW });
          },
          handleReviewGreen: (id, reviewGreen) => dispatch(updateNewsReview(id, { review_green: reviewGreen })),
        },
      })
    }

    result.push(...commonColumns);

    if ([TAB.SELECTED, TAB.ONLINE].includes(selectedTab)) {
      result.push({
        dataField: "selected_by",
        text: "Selected By",
        formatter: (cellContent) => cellContent?.name,
      })
    }

    if (TAB.DISCHARGED === selectedTab) {
      result.push({
        dataField: "discharged_by",
        text: "Discharged By",
        formatter: (cellContent) => cellContent?.name,
      })
    }

    if (TAB.REVIEW === selectedTab) {
      result.push({
        dataField: "status",
        text: "Status",
        formatter: (_, { selected_by, status, discharged_by }) => {
          const statusContent = {
            n: (
              <>
                <span>Online</span>
                {!!selected_by?.name && <span>({selected_by?.name})</span>}
              </>
            ),
            d: (
              <>
                <span>Discharged</span>
                {!!discharged_by?.name && <span>({discharged_by?.name})</span>}
              </>
            ),
          }

          return <div className="d-flex flex-column">{statusContent[status]}</div>
        },
        style: { minWidth: '140px' },
      })
    }

    result.push({
      dataField: "action",
      text: "Actions",
      formatter:
        selectedTab === 'new'
          ? columnFormatters.ActionsColumnFormatterSelect
          : columnFormatters.ActionsColumnFormatterEdit,
      formatExtraData: {
        openEditNewsPage: newsUIProps.openEditNewsPage,
        openSelectNewsPage: newsUIProps.openSelectNewsPage,
        openDeleteNewsDialog: selectedTab === 'review' ? null : newsUIProps.openDeleteNewsDialog,
        dischargeNews: (id) => dispatch(dischargeNews(id))
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    })

    return result;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedTab]);

  // Table pagination properties
  const paginationOptions = {
    totalSize: totalCount,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <PaginationProvider pagination={paginationFactory(paginationOptions)}>
      {({ paginationProps, paginationTableProps }) => (
        <BootstrapTable
          wrapperClasses="table-responsive"
          classes="table table-head-custom table-vertical-center overflow-hidden"
          remote
          bootstrap4
          bordered={false}
          keyField="id"
          data={entities || []}
          columns={columns}
          defaultSorted={uiHelpers.defaultSorted}
          onTableChange={getHandlerTableChange(newsUIProps.setQueryParams)}
          {...paginationTableProps}
        >
          <PleaseWaitMessage entities={entities} />
          <NoRecordsFoundMessage entities={entities} />
        </BootstrapTable>
      )}
    </PaginationProvider>
  );
}
