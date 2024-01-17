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
  pageListRenderer
} from "../../../../../../_metronic/_helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "../../../../../../_metronic/_partials/controls";

import { DocumentsAddEditModal } from "./DocumentsAddEditModal";
import { DocumentsDeleteDialog } from "./DocumentsDeleteDialog";

import * as columnFormatters from "./column-formatters";

export function DocumentsTable({ newsId }) {
  const [showDocumentsAddModal, setShowDocumentsAddModal] = useState(false);
  const [showDocumentsDeleteModal, setShowDocumentsDeleteModal] = useState(false);

  const [documents, setDocuments] = useState([]);

  const [selectedDocumentsId, setSelectedDocuments] = useState(null);
  const [selectedDocumentsIdDelete, setDocumentsIdDelete] = useState(null);

  const { documentList = [], newsDocuments = [] } = useSelector(
    state => ({
      documentList: state.news.documentList,
      newsDocuments: state.news.newsForEdit.documents,
    })
  );

  useEffect(() => {
    if (newsDocuments.length && documentList.length) {
      const relatedDocuments = newsDocuments.map(({ id: newsDocumentId }) =>
        documentList.find(({ id: documentId }) => documentId === newsDocumentId),
      );
      setDocuments(relatedDocuments)
    }
  }, [newsDocuments, documentList])


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
      dataField: "type",
      text: "Type",
      sort: true,
      formatter: cellContent => cellContent?.name,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditDocumentsPage: (id) => {
          setShowDocumentsAddModal(true);
          setSelectedDocuments(id);
        },
        openDeleteDocumentsDialog: (id) => {
          setDocumentsIdDelete(id);
          setShowDocumentsDeleteModal(true);
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
    totalSize: documents.length,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer
  };

  return (
    <>
      <Card>
        <CardHeader title="Attachments List">
          <CardHeaderToolbar>
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => {
                setSelectedDocuments(null);
                setShowDocumentsAddModal(true);
              }}
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
              data={documents}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={documents} />
              <NoRecordsFoundMessage entities={documents} />
            </BootstrapTable>
          )}
        </PaginationProvider>
      </Card>

      <DocumentsAddEditModal
        newsId={newsId}
        selectedDocumentsId={selectedDocumentsId}
        showDocumentsAddModal={showDocumentsAddModal}
        setShowDocumentsAddModal={setShowDocumentsAddModal}
      />

      <DocumentsDeleteDialog
        newsId={newsId}
        selectedDocumentsIdDelete={selectedDocumentsIdDelete}
        showDocumentsDeleteModal={showDocumentsDeleteModal}
        setShowDocumentsDeleteModal={setShowDocumentsDeleteModal}
      />
    </>
  );
}
