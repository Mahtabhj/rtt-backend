/* eslint-disable no-restricted-imports */
import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulation/regulationActions";

export function MilestoneDeleteDialog({
  selectedMilestoneIdDelete,
  showMilestoneDeleteModal,
  setShowMilestoneDeleteModal,
  regulationId,
}) {
  const dispatch = useDispatch();

  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.regulation.actionsLoading }),
    shallowEqual
  );

  // if !id we should close modal
  useEffect(() => {
    if (!selectedMilestoneIdDelete) {
      setShowMilestoneDeleteModal(false);
    }
  }, [selectedMilestoneIdDelete]);

  const deleteMilestone = () => {
    // server request for deleting milestone by id
    dispatch(actions.deleteRelatedMilestone(selectedMilestoneIdDelete)).then(
      () => {
        dispatch(actions.fetchRelatedMilestoneList(regulationId));
        setShowMilestoneDeleteModal(false);
      }
    );
  };

  return (
    <Modal
      show={showMilestoneDeleteModal}
      onHide={() => setShowMilestoneDeleteModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Milestone Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this milestone?</span>
        )}
        {isLoading && <span>Milestone is deleting...</span>}
      </Modal.Body>
      <Modal.Footer>
        <div>
          <button
            type="button"
            onClick={() => setShowMilestoneDeleteModal(false)}
            className="btn btn-light btn-elevate"
          >
            Cancel
          </button>
          <> </>
          <button
            type="button"
            onClick={deleteMilestone}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
