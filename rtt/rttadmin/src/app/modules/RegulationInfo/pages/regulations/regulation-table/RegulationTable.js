import React, { useEffect, useMemo, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";

import * as actions from "@redux-regulation/regulation/regulationActions";
import * as uiHelpers from "../RegulationUIHelpers";
import {
  getSelectRow,
  getHandlerTableChange,
  NoRecordsFoundMessage,
  PleaseWaitMessage,
} from "@metronic-helpers";
import { reviewStatus } from "@common";
import * as columnFormatters from "./column-formatters";
import { useRegulationUIContext } from "../RegulationUIContext";

export function RegulationTable() {
  const dispatch = useDispatch();

  const regulationUIContext = useRegulationUIContext();
  const regulationUIProps = useMemo(() => {
    return {
      ids: regulationUIContext.ids,
      setIds: regulationUIContext.setIds,
      queryParams: regulationUIContext.queryParams,
      setQueryParams: regulationUIContext.setQueryParams,
      openEditRegulationPage: regulationUIContext.openEditRegulationPage,
      openSelectRegulationPage: regulationUIContext.openSelectRegulationPage,
      openDeleteRegulationDialog:
        regulationUIContext.openDeleteRegulationDialog,
    };
  }, [regulationUIContext]);

  // Getting current state of regulation list from store (Redux)
  const { entities, totalCount } = useSelector(
    (state) => ({
      entities: state.regulation.entities,
      totalCount: state.regulation.totalCount,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.fetchMaterialCategoryList());
    dispatch(actions.fetchProductCategoryList());
    dispatch(actions.fetchDocumentsList());
    dispatch(actions.fetchURLsList());
    dispatch(actions.fetchRegulationTypeList());
    dispatch(actions.fetchStatusList());
    dispatch(actions.fetchLanguageList());
    dispatch(actions.fetchRegulatoryFrameworkList());
    dispatch(actions.fetchUserList());
  }, [dispatch]);

  // fixme first request on queryParams initialization, then another is formed based on the status, filter and search
  // figure out how to do one BE request on mount
  const [isInitialQuery, setIsInitialQuery] = useState(true);

  useEffect(() => {
    if (isInitialQuery) {
      setIsInitialQuery(false);
    } else {
      // clear selections list
      regulationUIProps.setIds([]);
      // server call by queryParams
      dispatch(actions.fetchRegulationList(regulationUIProps.queryParams));
    }
  }, [regulationUIProps.queryParams, isInitialQuery]);

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },
    {
      dataField: "name",
      text: "Regulation Name",
      sort: true,
    },
    {
      dataField: "regulatory_framework",
      text: "Framework",
      sort: true,
      formatter: (cellContent) => cellContent?.name,
    },
    {
      dataField: "description",
      text: "Description",
      sort: true,
      formatter: (cellContent) => (
        <div
          dangerouslySetInnerHTML={{ __html: cellContent }}
          style={{ maxHeight: '150px', overflow: 'hidden' }}
        />
      )
    },
    {
      dataField: "type",
      text: "type",
      sort: true,
      formatter: (cellContent) => cellContent?.name,
    },
    {
      dataField: "status",
      text: "status",
      sort: true,
      formatter: (cellContent) => cellContent?.name,
    },
    {
      dataField: "review_status",
      text: "Review Status",
      sort: true,
      formatter: (cellContent) => reviewStatus[cellContent],
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditRegulationPage: regulationUIProps.openEditRegulationPage,
        openSelectRegulationPage: regulationUIProps.openSelectRegulationPage,
        openDeleteRegulationDialog:
          regulationUIProps.openDeleteRegulationDialog,
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
              remote
              bootstrap4
              bordered={false}
              keyField="id"
              data={entities || []}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={getHandlerTableChange(
                regulationUIProps.setQueryParams
              )}
              selectRow={getSelectRow({
                entities,
                ids: regulationUIProps.ids,
                setIds: regulationUIProps.setIds,
              })}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={entities} />
              <NoRecordsFoundMessage entities={entities} />
            </BootstrapTable>
          );
        }}
      </PaginationProvider>
    </>
  );
}
