import React, { useMemo } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import { Modal } from "react-bootstrap";

import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-news/news/newsActions";

import { NewsRelevanceForm } from "./NewsRelevanceForm";

const initNewsRelevance = {
  organisation: "",
  news: "",
  relevancy: 0,
};

export function NewsRelevanceAddEditModal({
  newsId,
  showNewsRelevanceAddModal,
  setShowNewsRelevanceAddModal,
  selectedNewsRelevanceId,
  newsTitle,
}) {
  const history = useHistory();
  const dispatch = useDispatch();

  const {
    actionsLoading,
    newsRelevanceList = [],
  } = useSelector(
    (state) => ({
      actionsLoading: state.news.actionsLoading,
      newsRelevanceList: state.news.newsRelevanceList,
    })
  );

  const newsRelevance = useMemo(() =>
      selectedNewsRelevanceId
        ? newsRelevanceList.find(({ id }) => id === selectedNewsRelevanceId)
        : initNewsRelevance
  , [selectedNewsRelevanceId, newsRelevanceList])

  const saveNewsRelatedNewsRelevance = (values) => {
    if (!selectedNewsRelevanceId) {
      dispatch(
        actions.createNewsRelevance(values)
      ).then(() => {
        setShowNewsRelevanceAddModal(false);
        history.push(`/backend/news-info/impactAssessment`);
      });
    } else {
      dispatch(
        actions.updateNewsRelevance(values)
      ).then(() => {
        dispatch(actions.fetchNewsRelevanceList(newsId));
        setShowNewsRelevanceAddModal(false)
      });
    }
  };

  return (
    <Modal
      size="lg"
      show={showNewsRelevanceAddModal}
      onHide={() => setShowNewsRelevanceAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedNewsRelevanceId ? "Edit" : "Add"} News Relevance
        </Modal.Title>
        <Modal.Body>
          {newsTitle}
        </Modal.Body>
      </Modal.Header>

      <NewsRelevanceForm
        actionsLoading={actionsLoading}
        newsId={newsId}
        setShowNewsRelevanceAddModal={setShowNewsRelevanceAddModal}
        saveNewsRelatedNewsRelevance={saveNewsRelatedNewsRelevance}
        newsRelevance={newsRelevance}
      />
    </Modal>
  );
}
