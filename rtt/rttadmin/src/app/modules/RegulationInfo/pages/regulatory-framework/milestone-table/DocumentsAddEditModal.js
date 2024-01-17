import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import React, { useState } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import RichTextEditor from "react-rte";
import { DocumentsForm } from "../related-documents-table/DocumentsForm";
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
  setEmptyMilestone,
  emptyMilestone,
  document,
}) {
  const dispatch = useDispatch();
  const [isSaving, setIsSaving] = useState(false);
  const { actionsLoading } = useSelector(
    (state) => ({
      actionsLoading: state.regulation.actionsLoading,
    }),
    shallowEqual
  );

  const saveDocuments = (values) => {
    setIsSaving(true);
    const isDescriptionEmpty = values.description.toString("markdown").trim() === '\u200b';

    const payload = {
      ...values,
      description: isDescriptionEmpty ? '' : values.description.toString("html"),
    };

    dispatch(
      actions.createMilestoneDocument(payload, setEmptyMilestone, emptyMilestone)
    ).then(() => {
      setIsSaving(false);
      setShowDocumentsAddModal(false);
    });
  };

  const documentObj = document && {
    ...document,
    description: RichTextEditor.createValueFromString(document.description, "html")
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
          Add Documents
        </Modal.Title>
      </Modal.Header>
      <DocumentsForm
        setShowDocumentsAddModal={setShowDocumentsAddModal}
        saveRegulatoryFrameworkRelatedDocuments={saveDocuments}
        isSaving={isSaving}
        documents={documentObj}
      />
    </Modal>
  );
}
