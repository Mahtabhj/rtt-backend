/* eslint-disable no-restricted-imports */
import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulation/regulationActions";

export function UrlDeleteDialog({
  selectedUrlIdDelete,
  showUrlDeleteModal,
  setShowUrlDeleteModal,
  regulationId,
}) {
  const dispatch = useDispatch();

  const { regulationUrls = [], isLoading } = useSelector(({ regulation }) => ({
    regulationUrls: regulation.regulationForEdit?.urls,
    isLoading: regulation.actionsLoading,
  }));

  // if !id we should close modal
  useEffect(() => {
    if (!selectedUrlIdDelete) {
      setShowUrlDeleteModal(false);
    }
  }, [dispatch, selectedUrlIdDelete]);

  const deleteUrl = () => {
    dispatch(actions.updateRegulationField({
      id: regulationId,
      urls: regulationUrls.filter(({ id }) => id !== selectedUrlIdDelete).map(({ id }) => id),
    })).then(() => setShowUrlDeleteModal(false));
  };

  const handleOnHide = () => setShowUrlDeleteModal(false);

  return (
    <Modal
      show={showUrlDeleteModal}
      onHide={handleOnHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Regulation Url Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <span>{isLoading ? 'Url is deleting...' : 'Are you sure to permanently delete this Url?'}</span>
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
            onClick={deleteUrl}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
