import React from "react";

import { Modal } from "react-bootstrap";
import { ModalProgressBar } from "../../../../../../_metronic/_partials/controls";
import * as actions from "../../../_redux/news/newsActions";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import RichTextEditor from "react-rte";

import { ImpactAssessmentForm } from "./ImpactAssessmentForm";

const initImpactAssessment = {
  id: undefined,
  organisation: "",
  news: "",
  relevancy: "",
  comment: RichTextEditor.createEmptyValue(),
};

export function ImpactAssessmentAddEditModal({
  newsId,
  showImpactAssessmentAddModal,
  setShowImpactAssessmentAddModal,
  selectedImpactAssessmentId,
  newsTitle,
}) {
  const dispatch = useDispatch();

  const {
    actionsLoading,
    relatedNewsRelevance,
  } = useSelector(
    (state) => ({
      actionsLoading: state.news.actionsLoading,
      relatedNewsRelevance: (state.news.newsRelevanceList || []).find(
        (relevance) => relevance.id === selectedImpactAssessmentId
      ),
    }),
    shallowEqual
  );

  const saveNewsRelatedImpactAssessment = (values) => {
    if (!selectedImpactAssessmentId) {
      dispatch(
        actions.createNewsRelevance(values)
      ).then(() => setShowImpactAssessmentAddModal(false));
    } else {
      dispatch(
        actions.updateNewsRelevance(values)
      ).then(() => {
        dispatch(actions.fetchNewsRelevanceList(newsId));
        setShowImpactAssessmentAddModal(false)
      });
    }
  };

  return (
    <Modal
      size="lg"
      show={showImpactAssessmentAddModal}
      onHide={() => setShowImpactAssessmentAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedImpactAssessmentId ? "Edit" : "Add"} News Relevance
        </Modal.Title>
        <Modal.Body>
          {newsTitle}
        </Modal.Body>
      </Modal.Header>

      <ImpactAssessmentForm
        actionsLoading={actionsLoading}
        newsId={newsId}
        setShowImpactAssessmentAddModal={setShowImpactAssessmentAddModal}
        saveNewsRelatedImpactAssessment={
          saveNewsRelatedImpactAssessment
        }
        impactAssessment={relatedNewsRelevance ?
          {
            ...relatedNewsRelevance,
            comment: RichTextEditor.createValueFromString(relatedNewsRelevance.comment, "html")
          } : initImpactAssessment
        }
      />
    </Modal>
  );
}
