import {
  getHandlerTableChange,
  getSelectRow,
  NoRecordsFoundMessage,
  PleaseWaitMessage,
} from "@metronic-helpers";
import * as actions from "@redux-regulation/impact-assessment/impactAssessmentActions";
import React, { useEffect, useMemo } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { useImpactAssessmentUIContext } from "../ImpactAssessmentUIContext";
import * as uiHelpers from "../ImpactAssessmentUIHelpers";
import * as columnFormatters from "./column-formatters";

export function ImpactAssessmentTable() {
  const impactAssessmentUIContext = useImpactAssessmentUIContext();

  const impactAssessmentUIProps = useMemo(() => {
    return {
      ids: impactAssessmentUIContext.ids,
      setIds: impactAssessmentUIContext.setIds,
      queryParams: impactAssessmentUIContext.queryParams,
      setQueryParams: impactAssessmentUIContext.setQueryParams,
      openEditImpactAssessmentPage:
        impactAssessmentUIContext.openEditImpactAssessmentPage,
      openSelectImpactAssessmentPage:
        impactAssessmentUIContext.openSelectImpactAssessmentPage,
    };
  }, [impactAssessmentUIContext]);

  // Getting curret state of impactAssessment list from store (Redux)
  const { currentState } = useSelector(
    (state) => ({ currentState: state.impactAssessment }),
    shallowEqual
  );

  const { totalCount, entities } = currentState;

  // ImpactAssessment Redux state
  const dispatch = useDispatch();

  useEffect(() => {
    // clear selections list
    impactAssessmentUIProps.setIds([]);

    // server call by queryParams
    dispatch(
      actions.fetchImpactAssessmentList(impactAssessmentUIProps.queryParams)
    );

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [impactAssessmentUIProps.queryParams, dispatch]);

  const related_impactAssessment = [];

  entities &&
    entities.forEach((entity, index) => {
      const element = {
        id: index + 1,
        regions: entity.regulation.regions[0].name,
        regulation_name: entity.regulation.regulation_name,
        issuing_body: entity.regulation.issuing_body,
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
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditImpactAssessmentPage:
          impactAssessmentUIProps.openEditImpactAssessmentPage,
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
    totalSize: totalCount,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <PaginationProvider pagination={paginationFactory(paginationOptions)}>
        {({ paginationProps, paginationTableProps }) => {
          return (
            <BootstrapTable
              wrapperClasses="table-responsive"
              classes="table table-head-custom table-vertical-center overflow-hidden"
              bootstrap4
              bordered={false}
              remote
              keyField="id"
              data={
                related_impactAssessment === null
                  ? []
                  : related_impactAssessment
              }
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={getHandlerTableChange(
                impactAssessmentUIProps.setQueryParams
              )}
              selectRow={getSelectRow({
                entities,
                ids: impactAssessmentUIProps.ids,
                setIds: impactAssessmentUIProps.setIds,
              })}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={related_impactAssessment} />
              <NoRecordsFoundMessage entities={related_impactAssessment} />
            </BootstrapTable>
          );
        }}
      </PaginationProvider>
    </>
  );
}
