import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-news/news/newsActions";

export function NewsRelevanceDeleteDialog({
  selectedNewsRelevanceIdDelete,
  showNewsRelevanceDeleteModal,
  setShowNewsRelevanceDeleteModal,
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
    if (!selectedNewsRelevanceIdDelete) {
      setShowNewsRelevanceDeleteModal(false);
    }
  }, [selectedNewsRelevanceIdDelete, dispatch]);

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  const deleteNewsRelevance = () => {
    // server request for deleting news by id
    dispatch(actions.deleteNewsRelevance(selectedNewsRelevanceIdDelete)).then(() => {
      dispatch(actions.fetchNews(newsId));
      dispatch(actions.fetchNewsRelevanceList(newsId));

      setShowNewsRelevanceDeleteModal(false);
    });
  };

  return (
    <Modal
      show={showNewsRelevanceDeleteModal}
      onHide={() => setShowNewsRelevanceDeleteModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          News Relevance Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this News Relevance?</span>
        )}
        {isLoading && <span>News Relevance is deleting...</span>}
      </Modal.Body>
      <Modal.Footer>
        <div>
          <button
            type="button"
            onClick={() => setShowNewsRelevanceDeleteModal(false)}
            className="btn btn-light btn-elevate"
          >
            Cancel
          </button>
          <> </>
          <button
            type="button"
            onClick={deleteNewsRelevance}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
