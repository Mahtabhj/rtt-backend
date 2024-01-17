import React, { useEffect, useMemo, useRef, useState } from "react";
import { shallowEqual, useSelector } from "react-redux";
import ReactSelect from "react-select";
import PropTypes from "prop-types";
import BootstrapTable from "react-bootstrap-table-next";

import { NoRecordsFoundMessage, PleaseWaitMessage } from "@metronic-helpers";

import { documentColumnFormatters } from "./DocumentColumnFormatters";
import { DocumentsAddEditModal } from "./DocumentsAddEditModal";

const propTypes = {
  type: PropTypes.oneOf(['regulation', 'regulatoryFramework']).isRequired,
  selectedDocuments: PropTypes.array.isRequired,
  setSelectedDocuments: PropTypes.func.isRequired,
  documentOptions: PropTypes.array.isRequired,
}

export const SelectDocument = (
  {
    type,
    selectedDocuments,
    setSelectedDocuments,
    documentOptions,
    setUpdatedDocument
  }
) => {
  const { lastAddedDocument } = useSelector(
    (state) => ({
      lastAddedDocument: state[type].lastAddedDocument,
    }),
    shallowEqual
  );
  const refLastAddedDocument = useRef(null);

  const [showDocumentsAddModal, setShowDocumentsAddModal] = useState(false);
  const [documentIdToEdit, setDocumentIdToEdit] = useState(null);

  const formattedDocuments = useMemo(() => {
    return selectedDocuments.map(document => (
        { ...document, type: document.type?.name }
      )
    )
  }, [selectedDocuments]);

  useEffect(() => {
    if (lastAddedDocument && lastAddedDocument.id !== refLastAddedDocument.current?.id) {
      refLastAddedDocument.current = lastAddedDocument;

      const newSelectedDocuments = [...selectedDocuments, lastAddedDocument];
      setSelectedDocuments(newSelectedDocuments);
    }
  }, [refLastAddedDocument, lastAddedDocument, selectedDocuments]);

  const handleOnChangeSelectedDocuments = (document) => {
    const newSelectedDocuments = [...selectedDocuments];
    const index = newSelectedDocuments.findIndex(item => item.id === document.id);

    if (index < 0) {
      newSelectedDocuments.push(document);
    }

    setSelectedDocuments(newSelectedDocuments);
  };

  const handleOnRemoveDocument = (id) => {
    const newSelectedDocuments = selectedDocuments.filter(document => document.id !== id);
    setSelectedDocuments(newSelectedDocuments);
  };

  const handleOnCloseDocumentEditModal = () => {
    setShowDocumentsAddModal(false);
    setDocumentIdToEdit(null);
  }

  const handleOnClickNewDocument = () => setShowDocumentsAddModal(true);

  const columnsDocument = [
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
      formatter: (cellContent) => (
        <div
          dangerouslySetInnerHTML={{ __html: cellContent }}
          style={{ maxHeight: '150px', overflow: 'hidden' }}
        />
      )
    },
    {
      dataField: "type",
      text: "Type",
      sort: true,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: documentColumnFormatters,
      formatExtraData: {
        openEditDocumentsPage: (id) => {
          setShowDocumentsAddModal(true);
          setDocumentIdToEdit(id);
        },
        openDeleteDocumentsDialog: (id) => {
          handleOnRemoveDocument(id);
        },
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  return (
    <>
      <div className="row flex align-items-end">
        <div className="col-lg-10">
          <label>Select Document</label>
          <ReactSelect
            value={[]}
            getOptionLabel={(option) => option.title}
            getOptionValue={(option) => option.id}
            onChange={handleOnChangeSelectedDocuments}
            name="documents"
            options={documentOptions}
            className="basic-multi-select"
            classNamePrefix="select"
          />
        </div>

        <button
          type="button"
          onClick={handleOnClickNewDocument}
          className="btn btn-primary btn-elevate"
        >
          New document
        </button>
      </div>

      <BootstrapTable
        wrapperClasses="table-responsive"
        classes="table table-head-custom table-vertical-center overflow-hidden"
        bootstrap4
        bordered={false}
        keyField="id"
        data={formattedDocuments}
        columns={columnsDocument}
      >
        <PleaseWaitMessage entities={formattedDocuments} />
        <NoRecordsFoundMessage entities={formattedDocuments} />
      </BootstrapTable>

      <DocumentsAddEditModal
        type={type}
        showDocumentsAddModal={showDocumentsAddModal}
        document={documentOptions.find(document => document.id === documentIdToEdit)}
        setShowDocumentsAddModal={handleOnCloseDocumentEditModal}
        setUpdated={setUpdatedDocument}
      />
    </>
  )
}

SelectDocument.propTypes = propTypes;