import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import React, { useEffect, useState } from "react";
import { Modal } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { DocumentsForm } from "./DocumentsForm";
import RichTextEditor from 'react-rte';

const initDocuments = {
  id: undefined,
  title: "",
  description: RichTextEditor.createEmptyValue(),
  attachment: "",
  type: "",
};

export function DocumentsAddEditModal({
  showDocumentsAddModal,
  setShowDocumentsAddModal,
  selectedDocumentsId,
  regulatoryFrameworkId,
}) {
  const dispatch = useDispatch();

  const { actionsLoading, regulatoryFrameworkRelatedDocumentForEdit } = useSelector(
    ({ regulatoryFramework }) => ({
      actionsLoading: regulatoryFramework.actionsLoading,
      regulatoryFrameworkRelatedDocumentForEdit: regulatoryFramework.documentList.find(({ id }) => id === selectedDocumentsId),
    }),
  );

  const saveRegulatoryFrameworkRelatedDocuments = (values) => {
    const isDescriptionEmpty = values.description.toString("markdown").trim() === '\u200b';

    const payload = {
      ...values,
      description: isDescriptionEmpty ? '' : values.description.toString("html"),
    };

    const afterActionUpdate = () => {
      setShowDocumentsAddModal(false);
      dispatch(actions.fetchDocumentsList());
    };

    if (!selectedDocumentsId) {
      dispatch(
        actions.createRegulatoryFrameworkRelatedDocument({
          document: payload,
          regulatoryFrameworkId,
        })
      ).then(() => afterActionUpdate());
    } else {
      dispatch(actions.updateRegulatoryFrameworkRelatedDocument(payload)).then(() => afterActionUpdate());
    }
  };

  const document = regulatoryFrameworkRelatedDocumentForEdit && {
    ...regulatoryFrameworkRelatedDocumentForEdit,
    description: RichTextEditor.createValueFromString(regulatoryFrameworkRelatedDocumentForEdit.description, "html")
  } || initDocuments;

  return (
    <Modal
      size="lg"
      show={showDocumentsAddModal}
      onHide={() => setShowDocumentsAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedDocumentsId ? "Edit" : "Add"} Regulatory Framework Attachment
        </Modal.Title>
      </Modal.Header>

      <DocumentsForm
        setShowDocumentsAddModal={setShowDocumentsAddModal}
        saveRegulatoryFrameworkRelatedDocuments={saveRegulatoryFrameworkRelatedDocuments}
        documents={document}
        isSaving={actionsLoading}
      />
    </Modal>
  );
}
