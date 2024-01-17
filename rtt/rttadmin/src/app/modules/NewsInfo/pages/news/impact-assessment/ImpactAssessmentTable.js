import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";

import * as uiHelpers from "../NewsUIHelpers";
import {
  NoRecordsFoundMessage,
  PleaseWaitMessage,
  pageListRenderer,
} from "../../../../../../_metronic/_helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "../../../../../../_metronic/_partials/controls";

import { ImpactAssessmentAddEditModal } from "./ImpactAssessmentAddEditModal";
import { ImpactAssessmentDeleteDialog } from "./ImpactAssessmentDeleteDialog";

import * as columnFormatters from "./column-formatters";

export function ImpactAssessmentTable({ newsId, newsTitle }) {
  const [showImpactAssessmentAddModal, setShowImpactAssessmentAddModal] = useState(false);
  const [showImpactAssessmentDeleteModal, setShowImpactAssessmentDeleteModal] = useState(false);

  const [impactAssessment, setImpactAssessment] = useState([]);

  const [selectedImpactAssessmentId, setSelectedImpactAssessment] = useState(null);
  const [selectedImpactAssessmentIdDelete, setImpactAssessmentIdDelete] = useState(null);

  const { organizationList = [], newsRelevanceList = [] } = useSelector(
    state => ({
      organizationList: state.news.organizationList,
      newsRelevanceList: state.news.newsRelevanceList,
    }),
  );

  useEffect(() => {
    if (newsRelevanceList.length && organizationList.length) {
      const relatedImpactAssessment = newsRelevanceList
        .filter(({ news: newsItemId }) => newsItemId === newsId)
        .map(({ id, organization: organizationId, relevancy }) => ({
          id,
          organisation: organizationList.find(org => org.id === organizationId).name,
          news: newsTitle,
          relevancy,
        }));

      setImpactAssessment(relatedImpactAssessment);
    }
  }, [newsRelevanceList, organizationList])

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
          openEditImpactAssessmentPage: (id) => {
          setShowImpactAssessmentAddModal(true);
          setSelectedImpactAssessment(id);
        },
        openDeleteImpactAssessmentDialog: (id) => {
          setImpactAssessmentIdDelete(id);
          setShowImpactAssessmentDeleteModal(true);
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
    totalSize: impactAssessment.length,
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
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => {
                setSelectedImpactAssessment(null);
                setShowImpactAssessmentAddModal(true);
              }}
            >
              New Relevance
            </button>
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
              data={impactAssessment}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={impactAssessment} />
              <NoRecordsFoundMessage entities={impactAssessment} />
            </BootstrapTable>
          )}
        </PaginationProvider>
      </Card>

      <ImpactAssessmentAddEditModal
        newsTitle={newsTitle}
        newsId={newsId}
        selectedImpactAssessmentId={selectedImpactAssessmentId}
        showImpactAssessmentAddModal={showImpactAssessmentAddModal}
        setShowImpactAssessmentAddModal={setShowImpactAssessmentAddModal}
      />

      <ImpactAssessmentDeleteDialog
        newsId={newsId}
        selectedImpactAssessmentIdDelete={selectedImpactAssessmentIdDelete}
        showImpactAssessmentDeleteModal={showImpactAssessmentDeleteModal}
        setShowImpactAssessmentDeleteModal={setShowImpactAssessmentDeleteModal}
      />
    </>
  );
}
