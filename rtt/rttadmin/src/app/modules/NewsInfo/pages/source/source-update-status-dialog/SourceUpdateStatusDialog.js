import React, { useEffect, useState, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { SourceStatusCssClasses } from "../SourceUIHelpers";
import * as actions from "@redux-news/source/sourceActions";
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

export function SourceUpdateStatusDialog({ show, onHide }) {
  // Source UI Context
  const sourceUIContext = useSourceUIContext();
  const sourceUIProps = useMemo(() => {
    return {
      ids: sourceUIContext.ids,
      setIds: sourceUIContext.setIds,
      queryParams: sourceUIContext.queryParams,
    };
  }, [sourceUIContext]);

  // Source Redux state
  const { source, isLoading } = useSelector(
    (state) => ({
      source: selectedSource(state.source.entities, sourceUIProps.ids),
      isLoading: state.source.actionsLoading,
    }),
    shallowEqual
  );

  // if there weren't selected source we should close modal
  useEffect(() => {
    if (sourceUIProps.ids || sourceUIProps.ids.length === 0) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sourceUIProps.ids]);

  const [status, setStatus] = useState(0);

  const dispatch = useDispatch();
  const updateStatus = () => {
    // server request for updateing source by ids
    dispatch(actions.updateSourceStatus(sourceUIProps.ids, status)).then(() => {
      // refresh list after deletion
      dispatch(actions.fetchSource(sourceUIProps.queryParams)).then(() => {
        // clear selections list
        sourceUIProps.setIds([]);
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
          Status has been updated for selected source
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
      <Modal.Footer className="form">
        <div className="form-group">
          <select
            className={`form-control ${SourceStatusCssClasses[status]}`}
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
