/* eslint-disable no-restricted-imports */
import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";

export function RegulationDeleteDialog({
  selectedRegulationIdDelete,
  showRegulationDeleteModal,
  setShowRegulationDeleteModal,
  regulatoryFrameworkId,
}) {
  // Organization Redux state
  const dispatch = useDispatch();

  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.regulatoryFramework.actionsLoading }),
    shallowEqual
  );

  // if !id we should close modal
  useEffect(() => {
    if (!selectedRegulationIdDelete) {
      setShowRegulationDeleteModal(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedRegulationIdDelete, dispatch]);

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  const deleteRegulation = () => {
    // server request for deleting organization by id
    dispatch(
      actions.deleteRegulatoryFrameworkRelatedRegulation(
        selectedRegulationIdDelete
      )
    ).then(() => {
      dispatch(actions.fetchRelatedRegulationList(regulatoryFrameworkId));
      setShowRegulationDeleteModal(false);
    });
  };

  return (
    <Modal
      show={showRegulationDeleteModal}
      onHide={() => setShowRegulationDeleteModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Organization Regulation Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this regulation?</span>
        )}
        {isLoading && <span>Regulation is deleting...</span>}
      </Modal.Body>
      <Modal.Footer>
        <div>
          <button
            type="button"
            onClick={() => setShowRegulationDeleteModal(false)}
            className="btn btn-light btn-elevate"
          >
            Cancel
          </button>
          <> </>
          <button
            type="button"
            onClick={deleteRegulation}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
