import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Modal } from "react-bootstrap";

import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulation/regulationActions";

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
  regulationId,
}) {
  const dispatch = useDispatch();

  const { actionsLoading, regulationRelatedDocumentForEdit } = useSelector(
    ({ regulation }) => ({
      actionsLoading: regulation.actionsLoading,
      regulationRelatedDocumentForEdit: regulation.documentList?.find(({ id }) => id === selectedDocumentsId),
    }),
  );

  const saveRegulationRelatedDocuments = (values, typeSelected) => {
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
        actions.createRegulationRelatedDocument({
          document: payload,
          typeName: typeSelected.label,
          regulationId,
        })
      ).then(() => afterActionUpdate());
    } else {
      dispatch(
        actions.updateRegulationRelatedDocument({
          document: payload,
          typeName: typeSelected.label,
        })
      ).then(() => afterActionUpdate());
    }
  };

  const document = regulationRelatedDocumentForEdit && {
    ...regulationRelatedDocumentForEdit,
    description: RichTextEditor.createValueFromString(regulationRelatedDocumentForEdit.description, "html")
  } || initDocuments;

  const handleOnHide = () => setShowDocumentsAddModal(false);

  return (
    <Modal
      size="lg"
      show={showDocumentsAddModal}
      onHide={handleOnHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedDocumentsId ? "Edit" : "Add"} Regulation Attachment
        </Modal.Title>
      </Modal.Header>

      <DocumentsForm
        setShowDocumentsAddModal={setShowDocumentsAddModal}
        saveRegulationRelatedDocuments={saveRegulationRelatedDocuments}
        isSaving={actionsLoading}
        documents={document}
      />
    </Modal>
  );
}
