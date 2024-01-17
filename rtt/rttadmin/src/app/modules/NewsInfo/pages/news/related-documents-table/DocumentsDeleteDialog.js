/* eslint-disable no-restricted-imports */
import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "../../../../../../_metronic/_partials/controls";
import * as actions from "../../../_redux/news/newsActions";

export function DocumentsDeleteDialog({
  selectedDocumentsIdDelete,
  showDocumentsDeleteModal,
  setShowDocumentsDeleteModal,
  newsId,
}) {
  // News Redux state
  const dispatch = useDispatch();

  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.news.actionsLoading }),
    shallowEqual
  );

  // if !id we should close modal
  useEffect(() => {
    if (!selectedDocumentsIdDelete) {
      setShowDocumentsDeleteModal(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedDocumentsIdDelete, dispatch]);

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  const deleteDocuments = () => {
    // server request for deleting news by id
    dispatch(actions.deleteDocuments(selectedDocumentsIdDelete)).then(() => {
      dispatch(actions.fetchNews(newsId));
      setShowDocumentsDeleteModal(false);
    });
  };

  return (
    <Modal
      show={showDocumentsDeleteModal}
      onHide={() => setShowDocumentsDeleteModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          News Documents Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this document?</span>
        )}
        {isLoading && <span>Documents is deleting...</span>}
      </Modal.Body>
      <Modal.Footer>
        <div>
          <button
            type="button"
            onClick={() => setShowDocumentsDeleteModal(false)}
            className="btn btn-light btn-elevate"
          >
            Cancel
          </button>
          <> </>
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
