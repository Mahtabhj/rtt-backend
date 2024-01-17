/* eslint-disable no-restricted-imports */
import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Modal } from "react-bootstrap";

import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";

export function DocumentsDeleteDialog({
  selectedDocumentsIdDelete,
  showDocumentsDeleteModal,
  setShowDocumentsDeleteModal,
  regulatoryFrameworkId,
}) {
  const dispatch = useDispatch();

  const { isLoading, regulatoryFrameworkDocuments } = useSelector(({ regulatoryFramework }) => ({
    isLoading: regulatoryFramework.actionsLoading,
    regulatoryFrameworkDocuments: regulatoryFramework.regulatoryFrameworkForEdit.documents
  }));

  useEffect(() => {
    if (!selectedDocumentsIdDelete) {
      setShowDocumentsDeleteModal(false);
    }
  }, [dispatch, selectedDocumentsIdDelete]);

  const deleteDocuments = () => {
    dispatch(actions.updateRegulatoryFrameworkField({
      id: regulatoryFrameworkId,
      documents: regulatoryFrameworkDocuments.filter(({ id }) => id !== selectedDocumentsIdDelete).map(({ id }) => id),
    })).then(() => {
      setShowDocumentsDeleteModal(false);
    });
  };

  const handleOnHide = () => setShowDocumentsDeleteModal(false);

  return (
    <Modal
      show={showDocumentsDeleteModal}
      onHide={handleOnHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          RegulatoryFramework Documents Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <span>{isLoading ? 'Documents is deleting...' : 'Are you sure to permanently delete this document?'}</span>
      </Modal.Body>
      <Modal.Footer>
        <div>
          <button
            type="button"
            onClick={handleOnHide}
            className="btn btn-light btn-elevate"
            disabled={isLoading}
          >
            Cancel
          </button>

          <button
            type="button"
            onClick={deleteDocuments}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
