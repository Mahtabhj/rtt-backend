import React, { useMemo, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import RichTextEditor from "react-rte";
import { Modal } from "react-bootstrap";

import { ModalProgressBar } from "@metronic-partials/controls";
import {
  createMilestoneDocument as createRegulationMilestoneDocument,
  updateMilestoneDocument as updateRegulationMilestoneDocument
} from "@redux-regulation/regulation/regulationActions";
import {
  createMilestoneDocument as createRegulatoryFrameworkMilestoneDocument,
  updateMilestoneDocument as updateRegulatoryFrameworkMilestoneDocument,
} from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";

import { DocumentsForm } from "./DocumentForm";

const documentActions = {
  regulation: {
    createMilestoneDocument: createRegulationMilestoneDocument,
    updateMilestoneDocument: updateRegulationMilestoneDocument,
  },
  regulatoryFramework: {
    createMilestoneDocument: createRegulatoryFrameworkMilestoneDocument,
    updateMilestoneDocument: updateRegulatoryFrameworkMilestoneDocument,
  }
};


const initDocument = {
  id: undefined,
  title: "",
  description: RichTextEditor.createEmptyValue(),
  attachment: "",
  type: "",
};

export function DocumentsAddEditModal({
  type,
  showDocumentsAddModal,
  setShowDocumentsAddModal,
  document,
  setUpdated
}) {
  const dispatch = useDispatch();

  const [isSaving, setIsSaving] = useState(false);

  const { actionsLoading } = useSelector(
    (state) => ({
      actionsLoading: state[type].actionsLoading,
    }),
    shallowEqual
  );

  const documentObj = useMemo(() =>
    document
      ? {
          ...document,
          description: RichTextEditor.createValueFromString(document.description, "html")
      }
      : initDocument
    , [document]);

  const saveDocuments = (values) => {
    const isDescriptionEmpty = values.description.toString("markdown").trim() === '\u200b';
    const description = isDescriptionEmpty ? '' : values.description.toString("html");
    const valuesForRequest = { ...values, description: description, type: values.type.id };
    setIsSaving(true);

    const afterSaveAction = () => {
      setShowDocumentsAddModal(false);
      setIsSaving(false);
      setUpdated({ ...values, description: description });
    };

    if (values.id) {
      dispatch(
        documentActions[type].updateMilestoneDocument(valuesForRequest)
      ).then(() => {
        afterSaveAction();
      });
    } else {
      dispatch(
        documentActions[type].createMilestoneDocument(valuesForRequest)
      ).then(() => {
        afterSaveAction();
      });
    }
  };

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
        saveRelatedDocuments={saveDocuments}
        documents={documentObj}
        isSaving={isSaving}
      />
    </Modal>
  );
}
