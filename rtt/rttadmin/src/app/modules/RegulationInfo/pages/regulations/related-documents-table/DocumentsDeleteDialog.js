/* eslint-disable no-restricted-imports */
import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulation/regulationActions";

export function DocumentsDeleteDialog({
  selectedDocumentsIdDelete,
  showDocumentsDeleteModal,
  setShowDocumentsDeleteModal,
  regulationId,
}) {
  const dispatch = useDispatch();

  const { isLoading, regulationDocuments = [] } = useSelector(({ regulation }) => ({
    isLoading: regulation.actionsLoading,
    regulationDocuments: regulation.regulationForEdit.documents,
  }));

  // if !id we should close modal
  useEffect(() => {
    if (!selectedDocumentsIdDelete) {
      setShowDocumentsDeleteModal(false);
    }
  }, [selectedDocumentsIdDelete, dispatch]);

  const deleteDocuments = () => {
    dispatch(actions.updateRegulationField({
      id: regulationId,
      documents: regulationDocuments.filter(({ id }) => id !== selectedDocumentsIdDelete).map(({ id }) => id),
    })).then(() => setShowDocumentsDeleteModal(false));
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
          Regulation Documents Delete
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
