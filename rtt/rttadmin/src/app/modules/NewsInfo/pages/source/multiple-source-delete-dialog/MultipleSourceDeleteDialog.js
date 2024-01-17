/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-news/source/sourceActions";
import { useSourceUIContext } from "../SourceUIContext";

export function SourceDeleteDialog({ show, onHide }) {
  // Source UI Context
  const sourceUIContext = useSourceUIContext();
  const sourceUIProps = useMemo(() => {
    return {
      ids: sourceUIContext.ids,
      setIds: sourceUIContext.setIds,
      queryParams: sourceUIContext.queryParams,
    };
  }, [sourceUIContext]);

  // Source Redux state
  const dispatch = useDispatch();
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.source.actionsLoading }),
    shallowEqual
  );

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  // if there weren't selected source we should close modal
  useEffect(() => {
    if (!sourceUIProps.ids || sourceUIProps.ids.length === 0) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sourceUIProps.ids]);

  const deleteSource = () => {
    // server request for deleting source by seleted ids
    dispatch(actions.deleteSource(sourceUIProps.ids)).then(() => {
      // refresh list after deletion
      dispatch(actions.fetchSource(sourceUIProps.queryParams)).then(() => {
        // clear selections list
        sourceUIProps.setIds([]);
        // closing delete modal
        onHide();
      });
    });
  };

  return (
    <Modal
      show={show}
      onHide={onHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Source Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete selected source?</span>
        )}
        {isLoading && <span>Source are deleting...</span>}
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
            onClick={deleteSource}
            className="btn btn-primary btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
