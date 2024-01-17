/* eslint-disable no-restricted-imports */
import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";

export function LinkDeleteDialog({
  selectedLinkIdDelete,
  showLinkDeleteModal,
  setShowLinkDeleteModal,
  regulatoryFrameworkId,
}) {
  const dispatch = useDispatch();

  const { regulatoryFrameworkUrls = [], isLoading } = useSelector(({ regulatoryFramework }) => ({
    regulatoryFrameworkUrls: regulatoryFramework.regulatoryFrameworkForEdit?.urls,
    isLoading: regulatoryFramework.actionsLoading
  }));

  // if !id we should close modal
  useEffect(() => {
    if (!selectedLinkIdDelete) {
      setShowLinkDeleteModal(false);
    }
  }, [dispatch, selectedLinkIdDelete]);

  const deleteLink = () => {
    dispatch(actions.updateRegulatoryFrameworkField({
      id: regulatoryFrameworkId,
      urls: regulatoryFrameworkUrls.filter((url) => url.id !== selectedLinkIdDelete).map((url) => url.id),
    })).then(() => {
      setShowLinkDeleteModal(false);
    });
  };

  const handleOnHide = () => setShowLinkDeleteModal(false);

  return (
    <Modal
      show={showLinkDeleteModal}
      onHide={handleOnHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Organization Link Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <span>{isLoading ? 'Link is deleting...' : 'Are you sure to permanently delete this Link?'}</span>
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
            onClick={deleteLink}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
