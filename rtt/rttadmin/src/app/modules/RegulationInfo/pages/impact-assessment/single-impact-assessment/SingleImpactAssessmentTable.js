import React, { useMemo, useState } from "react";
import { useSelector } from "react-redux";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider } from "react-bootstrap-table2-paginator";

import { NoRecordsFoundMessage, PleaseWaitMessage } from "@metronic-helpers";

import * as uiHelpers from "../ImpactAssessmentUIHelpers";

import { Card } from "@metronic-partials/controls";

import { ActionsColumnFormatter } from "./column-formatters/ActionsColumnFormatter";
import { ImpactAssessmentAddEditModal } from "./ImpactAssessmentAddEditModal";

export function SingleImpactAssessmentTable({ impactAssessmentId }) {
  const [showImpactAssessmentAddModal, setShowImpactAssessmentAddModal] = useState(false);
  const [selectedQuestionsId, setSelectedQuestionsId] = useState(null);

  const { impactAssessments, regulations } = useSelector(
    (state) => ({
      impactAssessments: state.impactAssessment.entities,
      regulations: state.regulation.entities,
    }),
  );

  const singleImpactAssessment = useMemo(() =>
    impactAssessments && impactAssessments[impactAssessmentId]
  , [impactAssessmentId, impactAssessments]);

  let relatedRegulation =
    regulations &&
    singleImpactAssessment &&
    regulations.find(
      (reg) => reg.name === singleImpactAssessment.regulation.regulation_name
    );

  const related_impactAssessment = [];

  singleImpactAssessment &&
    singleImpactAssessment.questions.forEach((question, index) => {
      const element = {
        id: index + 1,
        regions: singleImpactAssessment.regulation.regions[0].name,
        regulation_name: singleImpactAssessment.regulation.regulation_name,
        issuing_body: singleImpactAssessment.regulation.issuing_body,
        organization_name: question.organization_name,
        open_questions: question.questions_count - question.answered,
        questions: question.questions,
      };

      related_impactAssessment.push(element);
    });

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },
    {
      dataField: "regulation_name",
      text: "Regulation",
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
      formatter: ActionsColumnFormatter,
      formatExtraData: {
        openEditImpactAssessmentPage: (id) => {
          setShowImpactAssessmentAddModal(true);
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
    // just exclude <, <<, >>, >
    const pageWithoutIndication = pages.filter(
      (p) => typeof p.page !== "string"
    );
    return (
      <div className="position-absolute" style={{ right: "1rem" }}>
        {pageWithoutIndication.map((p, id) => (
          <button
            key={id}
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
    // pageStartIndex: 0,
    // totalSize: totalCount,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <Card>
        <PaginationProvider pagination={paginationFactory(paginationOptions)}>
          {({ paginationTableProps }) => (
            <BootstrapTable
              wrapperClasses="table-responsive"
              classes="table table-head-custom table-vertical-center overflow-hidden"
              bootstrap4
              bordered={false}
              // remote
              keyField="id"
              data={related_impactAssessment || []}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={() => null}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={related_impactAssessment} />
              <NoRecordsFoundMessage entities={related_impactAssessment} />
            </BootstrapTable>
          )}
        </PaginationProvider>
      </Card>

      <ImpactAssessmentAddEditModal
        impactAssessmentId={impactAssessmentId}
        singleImpactAssessment={singleImpactAssessment}
        selectedQuestionsId={selectedQuestionsId}
        showImpactAssessmentAddModal={showImpactAssessmentAddModal}
        setShowImpactAssessmentAddModal={setShowImpactAssessmentAddModal}
        regulationId={relatedRegulation && relatedRegulation.id}
      />
    </>
  );
}
