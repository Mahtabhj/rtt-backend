import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";

import {
  NoRecordsFoundMessage,
  PleaseWaitMessage,
  pageListRenderer,
} from "@metronic-helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";

import * as actions from "@redux-news/news/newsActions";

import { NewsRelevanceAddEditModal } from "./NewsRelevanceAddEditModal";

import * as uiHelpers from "../../ImpactAssessmentUIHelpers";

import * as columnFormatters from "./column-formatters";

export function NewsRelevanceTable({ showNewRelevanceButton }) {
  const dispatch = useDispatch();

  const [newsRelevance, setNewsRelevance] = useState([]);

  const [selectedNewsRelevanceId, setSelectedNewsRelevance] = useState(null);
  const [showNewsRelevanceAddModal, setShowNewsRelevanceAddModal] = useState(false);

  const {
    newsForSelect: {
      id: newsId = null,
      title: newsTitle = ''
    } = {},
    organizationList = [],
    newsRelevanceList = [],
  } = useSelector(
    state => ({
      newsForSelect: state.news.newsForSelect,
      organizationList: state.news.organizationList,
      newsRelevanceList: state.news.newsRelevanceList,
    }),
  );

  useEffect(() => {
    dispatch(actions.fetchOrganizationList());
  }, [dispatch]);

  useEffect(() => {
    if (newsId) {
      dispatch(actions.fetchNewsRelevanceList(newsId));
    }
  }, [dispatch, newsId]);

  useEffect(() => {
    if (newsRelevanceList.length && organizationList.length) {
      const relatedNewsRelevance = newsRelevanceList
        .filter(({ news: newsItemId }) => newsItemId === newsId)
        .map(({ id, organization: organizationId, relevancy }) => ({
          id,
          organisation: organizationList.find(org => org.id === organizationId).name,
          news: newsTitle,
          relevancy,
        }));

      setNewsRelevance(relatedNewsRelevance);
    }
  }, [newsRelevanceList, organizationList]);

  const handleOpenNewRelevanceModal = () => {
    setSelectedNewsRelevance(null);
    setShowNewsRelevanceAddModal(true);
  }

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },
    {
      dataField: "organisation",
      text: "Organization",
      sort: true,
    },
    {
      dataField: "news",
      text: "News",
      sort: true,
    },

    {
      dataField: "relevancy",
      text: "Relevancy",
      sort: true,
    },

    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditNewsRelevancePage: (id) => {
          setShowNewsRelevanceAddModal(true);
          setSelectedNewsRelevance(id);
        },
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  const paginationOptions = {
    totalSize: newsRelevance.length,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer
  };

  return (
    <>
      <Card>
        <CardHeader title="News Relevance List">
          <CardHeaderToolbar>
            {showNewRelevanceButton &&
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleOpenNewRelevanceModal}
              >
                New Relevance
              </button>}
          </CardHeaderToolbar>
        </CardHeader>

        <PaginationProvider pagination={paginationFactory(paginationOptions)}>
          {({ paginationTableProps }) => (
            <BootstrapTable
              wrapperClasses="table-responsive"
              classes="table table-head-custom table-vertical-center overflow-hidden"
              bootstrap4
              bordered={false}
              keyField="id"
              data={newsRelevance}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={newsRelevance} />
              <NoRecordsFoundMessage entities={newsRelevance} />
            </BootstrapTable>
          )}
        </PaginationProvider>
      </Card>

      <NewsRelevanceAddEditModal
        newsTitle={newsTitle}
        newsId={newsId}
        selectedNewsRelevanceId={selectedNewsRelevanceId}
        showNewsRelevanceAddModal={showNewsRelevanceAddModal}
        setShowNewsRelevanceAddModal={setShowNewsRelevanceAddModal}
      />
    </>
  );
}
