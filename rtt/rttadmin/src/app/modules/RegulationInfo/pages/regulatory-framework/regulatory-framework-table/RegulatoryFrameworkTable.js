import React, { useEffect, useMemo, useState } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";

import { fetchRegulatoryFrameworkList } from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import * as uiHelpers from "../RegulatoryFrameworkUIHelpers";
import {
  getHandlerTableChange,
  NoRecordsFoundMessage,
  PleaseWaitMessage,
} from "@metronic-helpers";
import * as columnFormatters from "./column-formatters";
import { useRegulatoryFrameworkUIContext } from "../RegulatoryFrameworkUIContext";
import { reviewStatus } from "@common";


export function RegulatoryFrameworkTable() {
  const dispatch = useDispatch();

  // RegulatoryFramework UI Context
  const regulatoryFrameworkUIContext = useRegulatoryFrameworkUIContext();

  const regulatoryFrameworkUIProps = useMemo(() => {
    return {
      ids: regulatoryFrameworkUIContext.ids,
      setIds: regulatoryFrameworkUIContext.setIds,
      queryParams: regulatoryFrameworkUIContext.queryParams,
      setQueryParams: regulatoryFrameworkUIContext.setQueryParams,
      openEditRegulatoryFrameworkPage:
        regulatoryFrameworkUIContext.openEditRegulatoryFrameworkPage,
      openSelectRegulatoryFrameworkPage:
        regulatoryFrameworkUIContext.openSelectRegulatoryFrameworkPage,
      openDeleteRegulatoryFrameworkDialog:
        regulatoryFrameworkUIContext.openDeleteRegulatoryFrameworkDialog,
    };
  }, [regulatoryFrameworkUIContext]);

  // Getting current state of regulatoryFramework list from store (Redux)
  const  { totalCount, entities } = useSelector(
    (state) => ({
      totalCount: state.regulatoryFramework.totalCount,
      entities: state.regulatoryFramework.entities,
    }),
    shallowEqual
  );

  // fixme first request on queryParams initialization, then another is formed based on the status, filter and search
  // figure out how to do one BE request on mount
  const [isInitialQuery, setIsInitialQuery] = useState(true);

  useEffect(() => {
    if (isInitialQuery) {
      setIsInitialQuery(false);
    } else {
      // server call by queryParams
      dispatch(
        fetchRegulatoryFrameworkList(
          regulatoryFrameworkUIProps.queryParams
        )
      );
    }
  }, [dispatch, regulatoryFrameworkUIProps.queryParams, isInitialQuery]);

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },
    {
      dataField: "name",
      text: "Name",
      sort: true,
    },
    {
      dataField: "regions[0].name",
      text: "Region",
      sort: true,
    },
    {
      dataField: "issuing_body.name",
      text: "Issuing Body",
      sort: true,
    },
    {
      dataField: "regulation_regulatory_framework[0].name",
      text: "Regulation",
      sort: true,
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
        openEditRegulatoryFrameworkPage:
          regulatoryFrameworkUIProps.openEditRegulatoryFrameworkPage,
        openSelectRegulatoryFrameworkPage:
          regulatoryFrameworkUIProps.openSelectRegulatoryFrameworkPage,
        openDeleteRegulatoryFrameworkDialog:
          regulatoryFrameworkUIProps.openDeleteRegulatoryFrameworkDialog,
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

  const expandRow = {
    renderer: (row) => (
      <div className="d-flex justify-content-around flex-wrap">
        <div>
          <div>
            <strong>Issuing body:</strong>
            <div>{<p>{row.issuing_body.name}</p>}</div>
          </div>

          <div>
            <strong>Regions:</strong>
            <div>
              {row.regions.map((r, index) => (
                <p key={index}>{r.name}</p>
              ))}
            </div>
          </div>
        </div>

        <div>
          <div>
            <strong>Material categories:</strong>
            <div>
              {row.material_categories.map((mc, index) => (
                <p key={index}>{mc.name}</p>
              ))}
            </div>
          </div>
          <div>
            <strong>Product categories:</strong>
            <div>
              {row.product_categories.map((pc, index) => (
                <p key={index}>{pc.name}</p>
              ))}
            </div>
          </div>
        </div>
      </div>
    ),
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
              expandRow={expandRow}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={getHandlerTableChange(
                regulatoryFrameworkUIProps.setQueryParams
              )}
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
