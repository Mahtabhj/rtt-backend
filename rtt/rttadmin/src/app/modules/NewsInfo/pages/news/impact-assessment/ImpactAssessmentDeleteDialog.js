import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "../../../../../../_metronic/_partials/controls";
import * as actions from "../../../_redux/news/newsActions";

export function ImpactAssessmentDeleteDialog({
  selectedImpactAssessmentIdDelete,
  showImpactAssessmentDeleteModal,
  setShowImpactAssessmentDeleteModal,
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
    if (!selectedImpactAssessmentIdDelete) {
      setShowImpactAssessmentDeleteModal(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedImpactAssessmentIdDelete, dispatch]);

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  const deleteImpactAssessment = () => {
    // server request for deleting news by id
    dispatch(actions.deleteNewsRelevance(selectedImpactAssessmentIdDelete)).then(() => {
      dispatch(actions.fetchNews(newsId));
      dispatch(actions.fetchNewsRelevanceList(newsId));

      setShowImpactAssessmentDeleteModal(false);
    });
  };

  return (
    <Modal
      show={showImpactAssessmentDeleteModal}
      onHide={() => setShowImpactAssessmentDeleteModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          News ImpactAssessment Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this Impact Assessment?</span>
        )}
        {isLoading && <span>ImpactAssessment is deleting...</span>}
      </Modal.Body>
      <Modal.Footer>
        <div>
          <button
            type="button"
            onClick={() => setShowImpactAssessmentDeleteModal(false)}
            className="btn btn-light btn-elevate"
          >
            Cancel
          </button>
          <> </>
          <button
            type="button"
            onClick={deleteImpactAssessment}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
