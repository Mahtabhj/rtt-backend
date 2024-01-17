/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import { useRegulatoryFrameworkUIContext } from "../RegulatoryFrameworkUIContext";

export function RegulatoryFrameworkDeleteDialog({ id, show, onHide }) {
  // RegulatoryFramework UI Context
  const regulatoryFrameworkUIContext = useRegulatoryFrameworkUIContext();
  const regulatoryFrameworkUIProps = useMemo(() => {
    return {
      setIds: regulatoryFrameworkUIContext.setIds,
      queryParams: regulatoryFrameworkUIContext.queryParams,
    };
  }, [regulatoryFrameworkUIContext]);

  // RegulatoryFramework Redux state
  const dispatch = useDispatch();
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.regulatoryFramework.actionsLoading }),
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

  const deleteRegulatoryFramework = () => {
    // server request for deleting regulatoryFramework by id
    dispatch(actions.deleteRegulatoryFramework(id)).then(() => {
      // refresh list after deletion
      dispatch(
        actions.fetchRegulatoryFrameworkList(
          regulatoryFrameworkUIProps.queryParams
        )
      );
      // clear selections list
      regulatoryFrameworkUIProps.setIds([]);
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
          Regulatory Framework Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>
            Are you sure to permanently delete this Regulatory Framework?
          </span>
        )}
        {isLoading && <span>Regulatory Framework is deleting...</span>}
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
            onClick={deleteRegulatoryFramework}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
