/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-news/news/newsActions";
import { useNewsUIContext } from "../NewsUIContext";

export function NewsDeleteDialog({ id, show, onHide }) {
  // News UI Context
  const newsUIContext = useNewsUIContext();
  const newsUIProps = useMemo(() => {
    return {
      setIds: newsUIContext.setIds,
      queryParams: newsUIContext.queryParams,
    };
  }, [newsUIContext]);

  // News Redux state
  const dispatch = useDispatch();
  const { isLoading, tab } = useSelector(
    (state) => ({ isLoading: state.news.actionsLoading, tab: state.news.tab }),
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

  const deleteNews = () => {
    // server request for deleting news by id
    dispatch(actions.deleteNews(id)).then(() => {
      // refresh list after deletion
      dispatch(
        actions.fetchNewsList(
          tab === "new"
            ? { status: "n" }
            : tab === "selected"
            ? { status: "s" }
            : { status: "d" }
        )
      );
      // clear selections list
      newsUIProps.setIds([]);
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
        <Modal.Title id="example-modal-sizes-title-lg">News Delete</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this news?</span>
        )}
        {isLoading && <span>News is deleting...</span>}
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
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
