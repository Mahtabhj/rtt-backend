/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-news/news/newsActions";
import { useNewsUIContext } from "../NewsUIContext";

export function NewsDeleteDialog({ show, onHide }) {
  // News UI Context
  const newsUIContext = useNewsUIContext();
  const newsUIProps = useMemo(() => {
    return {
      ids: newsUIContext.ids,
      setIds: newsUIContext.setIds,
      queryParams: newsUIContext.queryParams,
    };
  }, [newsUIContext]);

  // News Redux state
  const dispatch = useDispatch();
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.news.actionsLoading }),
    shallowEqual
  );

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  // if there weren't selected news we should close modal
  useEffect(() => {
    if (!newsUIProps.ids || newsUIProps.ids.length === 0) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [newsUIProps.ids]);

  const deleteNews = () => {
    // server request for deleting news by seleted ids
    dispatch(actions.deleteNews(newsUIProps.ids)).then(() => {
      // refresh list after deletion
      dispatch(actions.fetchNews(newsUIProps.queryParams)).then(() => {
        // clear selections list
        newsUIProps.setIds([]);
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
        <Modal.Title id="example-modal-sizes-title-lg">News Delete</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete selected news?</span>
        )}
        {isLoading && <span>News are deleting...</span>}
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
            onClick={deleteNews}
            className="btn btn-primary btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
