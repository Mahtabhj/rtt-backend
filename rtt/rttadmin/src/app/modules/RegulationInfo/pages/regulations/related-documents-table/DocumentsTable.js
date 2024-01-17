import React, { useState } from "react";
import { useSelector } from "react-redux";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider } from "react-bootstrap-table2-paginator";

import { NoRecordsFoundMessage, PleaseWaitMessage, pageListRenderer } from "@metronic-helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";

import * as uiHelpers from "../RegulationUIHelpers";
import * as columnFormatters from "./column-formatters";
import { DocumentsAddEditModal } from "./DocumentsAddEditModal";
import { DocumentsDeleteDialog } from "./DocumentsDeleteDialog";
import { DocumentsLinkDocumentModal } from './DocumentsLinkDocumentModal';

export function DocumentsTable({ regulationId }) {
  const regulationDocuments = useSelector((state) => state?.regulation?.regulationForEdit?.documents || []);

  const [showDocumentsAddModal, setShowDocumentsAddModal] = useState(false);
  const [showDocumentsDeleteModal, setShowDocumentsDeleteModal] = useState(false);
  const [showLinkDocumentModal, setShowLinkDocumentModal] = useState(false);

  const [selectedDocumentsId, setSelectedDocuments] = useState(null);
  const [selectedDocumentsIdDelete, setDocumentsIdDelete] = useState(null);

  const handleOpenLinkDocuments = () => {
    setSelectedDocuments(null);
    setShowLinkDocumentModal(true);
  };

  const handleOpenAddDocumentsPage = () => {
    setSelectedDocuments(null);
    setShowDocumentsAddModal(true);
  };

  const handleOpenEditDocumentsPage = id => {
    setSelectedDocuments(id);
    setShowDocumentsAddModal(true);
  };

  const handleOpenDeleteDocumentsDialog = id => {
    setDocumentsIdDelete(id);
    setShowDocumentsDeleteModal(true);
  };

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },
    {
      dataField: "title",
      text: "Title",
      sort: true,
    },
    {
      dataField: "description",
      text: "Description",
      sort: true,
      formatter: (cellContent) => <div dangerouslySetInnerHTML={{ __html: cellContent }} style={{ maxHeight: '150px', overflow: 'hidden' }} />
    },
    {
      dataField: "type",
      text: "Type",
      sort: true,
      formatter: (cellContent) => cellContent?.name,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditDocumentsPage: handleOpenEditDocumentsPage,
        openDeleteDocumentsDialog: handleOpenDeleteDocumentsDialog,
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  const paginationOptions = {
    totalSize: regulationDocuments?.length,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <Card>
        <CardHeader title="Attachments List">
          <CardHeaderToolbar>
            <button
              style={{ marginRight: '10px' }}
              type="button"
              className="btn btn-primary"
              onClick={handleOpenLinkDocuments}
            >
              Link Attachments
            </button>

            <button
              type="button"
              className="btn btn-primary"
              onClick={handleOpenAddDocumentsPage}
            >
              New Attachments
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
              data={regulationDocuments}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={() => null}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={regulationDocuments} />
              <NoRecordsFoundMessage entities={regulationDocuments} />
            </BootstrapTable>
          )}
        </PaginationProvider>
      </Card>

      <DocumentsLinkDocumentModal
        regulationId={regulationId}
        showLinkDocumentModal={showLinkDocumentModal}
        setShowLinkDocumentModal={setShowLinkDocumentModal}
        idsOfSelectedDocuments={regulationDocuments.map(({ id }) => id)}
      />

      <DocumentsAddEditModal
        regulationId={regulationId}
        selectedDocumentsId={selectedDocumentsId}
        showDocumentsAddModal={showDocumentsAddModal}
        setShowDocumentsAddModal={setShowDocumentsAddModal}
      />

      <DocumentsDeleteDialog
        regulationId={regulationId}
        selectedDocumentsIdDelete={selectedDocumentsIdDelete}
        showDocumentsDeleteModal={showDocumentsDeleteModal}
        setShowDocumentsDeleteModal={setShowDocumentsDeleteModal}
      />
    </>
  );
}
