import React, { useState } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { useSelector } from "react-redux";
import * as uiHelpers from "../RegulationUIHelpers";
import { NoRecordsFoundMessage, PleaseWaitMessage } from "@metronic-helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";

import { ImpactAssessmentAddEditModal } from "./ImpactAssessmentAddEditModal";

import * as columnFormatters from "./column-formatters";

export function ImpactAssessmentTable({ regulationId }) {
  // Getting current state of organization users list from store (Redux)
  const { currentState } = useSelector(
    state => ({
      currentState: state.regulation.regulationImpactAssessmentForEdit
    }), []
  );

  const related_impactAssessment = [];

  currentState && currentState.questions.forEach((question, index) => {
    const element = {
      id: index + 1,
      regions: currentState.regulation.regions[0].name,
      regulation_name: currentState.regulation.regulation_name,
      issuing_body: currentState.regulation.issuing_body,
      organization_name: question.organization_name,
      open_questions: question.questions_count - question.answered,
      questions: question.questions,
    };

    related_impactAssessment.push(element);
  });

  const [showImpactAssessmentAddModal, setShowImpactAssessmentAddModal] = useState(false);

  const [selectedQuestionsId, setSelectedQuestionsId] = useState(null);

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },

    {
      dataField: "regions",
      text: "Region",
      sort: true,
    },
    {
      dataField: "regulation_name",
      text: "Regulation",
      sort: true,
    },
    {
      dataField: "issuing_body",
      text: "Issuing Body",
      sort: true,
    },
    {
      dataField: "organization_name",
      text: "Organization",
      sort: true,
    },
    {
      dataField: "open_questions",
      text: "Open Questions",
      sort: true,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditImpactAssessmentPage: (id) => {
          setShowImpactAssessmentAddModal(true);
          setSelectedQuestionsId(id);
        },
        openDeleteImpactAssessmentDialog: (id) => {
          setSelectedQuestionsId(id);
        },
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  const pageListRenderer = ({ pages, onPageChange }) => {
    const pageWithoutIndication = pages.filter(
      (p) => typeof p.page !== "string"
    );
    return (
      <div className="position-absolute" style={{ right: "1rem" }}>
        {pageWithoutIndication.map((p, index) => (
          <button
            key={index}
            className="btn btn-primary ml-1 pt-2 pb-2 pr-3 pl-3"
            onClick={() => onPageChange(p.page)}
          >
            {p.page}
          </button>
        ))}
      </div>
    );
  };

  const paginationOptions = {
    totalSize: related_impactAssessment && related_impactAssessment.length,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <Card>
        <CardHeader title="Impact Assessment List">
          <CardHeaderToolbar />
        </CardHeader>

        <PaginationProvider pagination={paginationFactory(paginationOptions)}>
          {({ paginationProps, paginationTableProps }) => {
            return (
              <BootstrapTable
                wrapperClasses="table-responsive"
                classes="table table-head-custom table-vertical-center overflow-hidden"
                bootstrap4
                bordered={false}
                keyField="id"
                data={
                  related_impactAssessment === undefined
                    ? []
                    : related_impactAssessment
                }
                columns={columns}
                defaultSorted={uiHelpers.defaultSorted}
                onTableChange={() => null}
                {...paginationTableProps}
              >
                <PleaseWaitMessage entities={related_impactAssessment} />
                <NoRecordsFoundMessage entities={related_impactAssessment} />
              </BootstrapTable>
            );
          }}
        </PaginationProvider>
      </Card>

      <ImpactAssessmentAddEditModal
        regulationId={regulationId}
        selectedQuestionsId={selectedQuestionsId}
        showImpactAssessmentAddModal={showImpactAssessmentAddModal}
        setShowImpactAssessmentAddModal={setShowImpactAssessmentAddModal}
      />
    </>
  );
}
