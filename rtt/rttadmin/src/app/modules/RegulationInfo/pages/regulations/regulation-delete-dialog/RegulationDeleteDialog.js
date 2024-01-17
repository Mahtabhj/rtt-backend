/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulation/regulationActions";
import { useRegulationUIContext } from "../RegulationUIContext";

export function RegulationDeleteDialog({ id, show, onHide }) {
  // Regulation UI Context
  const regulationUIContext = useRegulationUIContext();
  const regulationUIProps = useMemo(() => {
    return {
      setIds: regulationUIContext.setIds,
      queryParams: regulationUIContext.queryParams,
    };
  }, [regulationUIContext]);

  // Regulation Redux state
  const dispatch = useDispatch();
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.regulation.actionsLoading }),
    shallowEqual
  );

  // if !id we should close modal
  useEffect(() => {
    if (!id) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  const deleteRegulation = () => {
    // server request for deleting regulation by id
    dispatch(actions.deleteRegulation(id)).then(() => {
      // refresh list after deletion
      dispatch(actions.fetchRegulationList(regulationUIProps.queryParams));
      // clear selections list
      regulationUIProps.setIds([]);
      // closing delete modal
      onHide();
    });
  };

  return (
    <Modal
      show={show}
      onHide={onHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Regulation Delete
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
            onClick={onHide}
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
