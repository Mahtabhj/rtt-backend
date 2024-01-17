import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useSelector } from "react-redux";
import { SourceStatusCssClasses } from "../SourceUIHelpers";
import { useSourceUIContext } from "../SourceUIContext";

const selectedSource = (entities, ids) => {
  const _source = [];
  ids.forEach((id) => {
    const source = entities.find((el) => el.id === id);
    if (source) {
      _source.push(source);
    }
  });
  return _source;
};

export function SourceFetchDialog({ show, onHide }) {
  // Source UI Context
  const sourceUIContext = useSourceUIContext();
  const sourceUIProps = useMemo(() => {
    return {
      ids: sourceUIContext.ids,
      queryParams: sourceUIContext.queryParams,
    };
  }, [sourceUIContext]);

  // Source Redux state
  const { source } = useSelector(
    (state) => ({
      source: selectedSource(state.source.entities, sourceUIProps.ids),
    }),
    shallowEqual
  );

  // if there weren't selected ids we should close modal
  useEffect(() => {
    if (!sourceUIProps.ids || sourceUIProps.ids.length === 0) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sourceUIProps.ids]);

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
            {source.map((source) => (
              <div className="list-timeline-item mb-3" key={source.id}>
                <span className="list-timeline-text">
                  <span
                    className={`label label-lg label-light-${
                      SourceStatusCssClasses[source.status]
                    } label-inline`}
                    style={{ width: "60px" }}
                  >
                    ID: {source.id}
                  </span>{" "}
                  <span className="ml-5">
                    {source.manufacture}, {source.model}
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
