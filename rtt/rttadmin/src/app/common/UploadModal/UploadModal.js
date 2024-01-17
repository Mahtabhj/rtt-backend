import React from "react";
import { Modal } from "react-bootstrap";
import PropTypes from "prop-types";

import { ModalProgressBar } from "@metronic-partials/controls";
import { UploadFile } from "../UploadFile/UploadFile";

const propTypes = {
  title: PropTypes.string.isRequired,
  isModalShown: PropTypes.bool.isRequired,
  file: PropTypes.object,
  setFile: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  actionsLoading: PropTypes.bool.isRequired,
}

const defaultProps = {
  file: null,
}

export const UploadModal = ({ title, isModalShown, file, setFile, onClose, onSubmit, actionsLoading }) => {
  return isModalShown && (
    <Modal
      size="lg"
      show={isModalShown}
      onHide={onClose}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}

      <Modal.Header>
        <Modal.Title id="example-modal-sizes-title-lg">{title}</Modal.Title>
      </Modal.Header>

      <Modal.Body className="overlay overlay-block cursor-default">
        <UploadFile file={file} setFile={setFile} progress={0} />
      </Modal.Body>

      <Modal.Footer>
        <button
          type="button"
          onClick={onClose}
          className="btn btn-light btn-elevate"
        >
          Cancel
        </button>

        <button
          type="submit"
          onClick={onSubmit}
          className="btn btn-primary btn-elevate"
          style={{ minWidth: '100px' }}
        >
          Save
          {actionsLoading && (<span className="ml-3 spinner spinner-white" />)}
        </button>
      </Modal.Footer>
    </Modal>
  );
}

UploadModal.propTypes = propTypes;
UploadModal.defaultProps = defaultProps;
