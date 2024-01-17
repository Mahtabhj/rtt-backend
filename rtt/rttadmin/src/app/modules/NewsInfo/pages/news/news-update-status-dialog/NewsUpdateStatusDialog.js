import React, { useEffect, useState, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { NewsStatusCssClasses } from "../NewsUIHelpers";
import * as actions from "@redux-news/news/newsActions";
import { useNewsUIContext } from "../NewsUIContext";

const selectedNews = (entities, ids) => {
  const _news = [];
  ids.forEach((id) => {
    const news = entities.find((el) => el.id === id);
    if (news) {
      _news.push(news);
    }
  });
  return _news;
};

export function NewsUpdateStatusDialog({ show, onHide }) {
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
  const { news, isLoading } = useSelector(
    (state) => ({
      news: selectedNews(state.news.entities, newsUIProps.ids),
      isLoading: state.news.actionsLoading,
    }),
    shallowEqual
  );

  // if there weren't selected news we should close modal
  useEffect(() => {
    if (newsUIProps.ids || newsUIProps.ids.length === 0) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [newsUIProps.ids]);

  const [status, setStatus] = useState(0);

  const dispatch = useDispatch();
  const updateStatus = () => {
    // server request for updateing news by ids
    dispatch(actions.updateNewsStatus(newsUIProps.ids, status)).then(() => {
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
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Status has been updated for selected news
        </Modal.Title>
      </Modal.Header>
      <Modal.Body className="overlay overlay-block cursor-default">
        {isLoading && (
          <div className="overlay-layer bg-transparent">
            <div className="spinner spinner-lg spinner-warning" />
          </div>
        )}
        <div className="list-timeline list-timeline-skin-light padding-30">
          <div className="list-timeline-items">
            {news.map((news) => (
              <div className="list-timeline-item mb-3" key={news.id}>
                <span className="list-timeline-text">
                  <span
                    className={`label label-lg label-light-${
                      NewsStatusCssClasses[news.status]
                    } label-inline`}
                    style={{ width: "60px" }}
                  >
                    ID: {news.id}
                  </span>{" "}
                  <span className="ml-5">
                    {news.manufacture}, {news.model}
                  </span>
                </span>
              </div>
            ))}
          </div>
        </div>
      </Modal.Body>
      <Modal.Footer className="form">
        <div className="form-group">
          <select
            className={`form-control ${NewsStatusCssClasses[status]}`}
            value={status}
            onChange={(e) => setStatus(+e.target.value)}
          >
            <option value="0">Selling</option>
            <option value="1">Sold</option>
          </select>
        </div>
        <div className="form-group">
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
            onClick={updateStatus}
            className="btn btn-primary btn-elevate"
          >
            Update Status
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
