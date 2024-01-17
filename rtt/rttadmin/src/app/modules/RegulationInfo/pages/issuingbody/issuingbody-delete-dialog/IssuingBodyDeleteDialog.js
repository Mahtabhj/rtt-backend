/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/issuingbody/issuingbodyActions";
import { useIssuingBodyUIContext } from "../IssuingBodyUIContext";

export function IssuingBodyDeleteDialog({ id, show, onHide }) {
  // IssuingBody UI Context
  const issuingbodyUIContext = useIssuingBodyUIContext();
  const issuingbodyUIProps = useMemo(() => {
    return {
      setIds: issuingbodyUIContext.setIds,
      queryParams: issuingbodyUIContext.queryParams,
    };
  }, [issuingbodyUIContext]);

  // IssuingBody Redux state
  const dispatch = useDispatch();
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.issuingbody.actionsLoading }),
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

  const deleteIssuingBody = () => {
    // server request for deleting issuingbody by id
    dispatch(actions.deleteIssuingBody(id)).then(() => {
      // refresh list after deletion
      dispatch(actions.fetchIssuingBodyList(issuingbodyUIProps.queryParams));
      // clear selections list
      issuingbodyUIProps.setIds([]);
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
          IssuingBody Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this issuingbody?</span>
        )}
        {isLoading && <span>IssuingBody is deleting...</span>}
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
            onClick={deleteIssuingBody}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
