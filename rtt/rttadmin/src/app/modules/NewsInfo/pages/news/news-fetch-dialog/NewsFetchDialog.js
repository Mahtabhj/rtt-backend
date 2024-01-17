import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useSelector } from "react-redux";
import { NewsStatusCssClasses } from "../NewsUIHelpers";
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

export function NewsFetchDialog({ show, onHide }) {
  // News UI Context
  const newsUIContext = useNewsUIContext();
  const newsUIProps = useMemo(() => {
    return {
      ids: newsUIContext.ids,
      queryParams: newsUIContext.queryParams,
    };
  }, [newsUIContext]);

  // News Redux state
  const { news } = useSelector(
    (state) => ({
      news: selectedNews(state.news.entities, newsUIProps.ids),
    }),
    shallowEqual
  );

  // if there weren't selected ids we should close modal
  useEffect(() => {
    if (!newsUIProps.ids || newsUIProps.ids.length === 0) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [newsUIProps.ids]);

  return (
    <Modal
      show={show}
      onHide={onHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Fetch selected elements
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
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
            onClick={onHide}
            className="btn btn-primary btn-elevate"
          >
            Ok
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
