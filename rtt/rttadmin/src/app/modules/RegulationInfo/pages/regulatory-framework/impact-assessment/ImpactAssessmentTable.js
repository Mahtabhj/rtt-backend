import React, { useState } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useSelector } from "react-redux";
import * as uiHelpers from "../RegulatoryFrameworkUIHelpers";
import {
  NoRecordsFoundMessage,
  PleaseWaitMessage,
} from "../../../../../../_metronic/_helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "../../../../../../_metronic/_partials/controls";
import { ImpactAssessmentAddEditModal } from "./ImpactAssessmentAddEditModal";
import * as columnFormatters from "./column-formatters";

export function ImpactAssessmentTable({ regulatoryFrameworkId }) {
  // Organization UI Context

  // Getting curret state of organization users list from store (Redux)
  const { rfImpactAssessment } = useSelector(
    (state) => ({
      rfImpactAssessment:
        state.regulatoryFramework.regulatoryFrameworkImpactAssessmentForEdit,
      relatedRegulation: state.regulatoryFramework.related_regulation,
    }),
    shallowEqual
  );
  const related_impactAssessment = [];

  rfImpactAssessment.questions.forEach((question, index) => {
    const element = {
      id: index + 1,
      organization_name: question.organization_name,
      questions: question.questions,
    };
    related_impactAssessment.push(element);
  });

  // Organization Redux state
  const [
    showImpactAssessmentAddModal,
    setShowImpactAssessmentAddModal,
  ] = useState(false);
  const [selectedQuestionsId, setSelectedQuestionsId] = useState(null);

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },
    {
      dataField: "organization_name",
      text: "Organization",
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
        {pageWithoutIndication.map((p) => (
          <button
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
          <CardHeaderToolbar></CardHeaderToolbar>
        </CardHeader>

        <PaginationProvider pagination={paginationFactory(paginationOptions)}>
          {({ paginationTableProps }) => {
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
        regulatoryFrameworkId={regulatoryFrameworkId}
        selectedQuestionsId={selectedQuestionsId}
        showImpactAssessmentAddModal={showImpactAssessmentAddModal}
        setShowImpactAssessmentAddModal={setShowImpactAssessmentAddModal}
      />
    </>
  );
}
