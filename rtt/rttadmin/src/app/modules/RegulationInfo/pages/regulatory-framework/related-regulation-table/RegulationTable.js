import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider } from "react-bootstrap-table2-paginator";

import * as actions from "../../../_redux/regulatory-framework/regulatoryFrameworkActions";
import * as uiHelpers from "../../regulatory-framework/RegulatoryFrameworkUIHelpers";

import { NoRecordsFoundMessage, PleaseWaitMessage, pageListRenderer } from "@metronic-helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";

import * as columnFormatters from "./column-formatters";

import { RegulationAddModalButton } from "./RegulationAddModalButton";
import { RegulationDeleteDialog } from "./RegulationDeleteDialog";

export function RegulationTable({ regulatoryFrameworkId }) {
  const dispatch = useDispatch();

  const relatedRegulations = useSelector(state => state.regulatoryFramework.related_regulation || []);

  const [showRegulationDeleteModal, setShowRegulationDeleteModal] = useState(false);

  const [selectedRegulationIdDelete, setRegulationIdDelete] = useState(null);

  useEffect(() => {
    dispatch(actions.fetchRelatedRegulationList(regulatoryFrameworkId));
  }, [regulatoryFrameworkId, dispatch]);

  const handleOpenEditRegulationPage = id => window.open(`/backend/regulation-info/regulation/${id}/edit`, "_blank");

  const handleOpenDeleteRegulationDialog = id => {
    setRegulationIdDelete(id);
    setShowRegulationDeleteModal(true);
  };

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
      dataField: "review_status",
      text: "Review Status",
      sort: true,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditRegulationPage: handleOpenEditRegulationPage,
        openDeleteRegulationDialog: handleOpenDeleteRegulationDialog,
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  // Table pagination properties
  const paginationOptions = {
    totalSize: relatedRegulations?.length,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <Card>
        <CardHeader title="Regulations list">
          <CardHeaderToolbar>
            <RegulationAddModalButton regulatoryFrameworkId={regulatoryFrameworkId} />
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
              data={relatedRegulations}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={() => null}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={relatedRegulations} />
              <NoRecordsFoundMessage entities={relatedRegulations} />
            </BootstrapTable>
          )}
        </PaginationProvider>
      </Card>

      {showRegulationDeleteModal && (
        <RegulationDeleteDialog
          regulatoryFrameworkId={regulatoryFrameworkId}
          selectedRegulationIdDelete={selectedRegulationIdDelete}
          showRegulationDeleteModal={showRegulationDeleteModal}
          setShowRegulationDeleteModal={setShowRegulationDeleteModal}
        />
      )}
    </>
  );
}
