import React from "react";
import { Modal } from "react-bootstrap";
import PropTypes from "prop-types";

const propTypes = {
  isShown: PropTypes.bool.isRequired,
  isLoading: PropTypes.bool.isRequired,
  onSubmitCallback: PropTypes.func.isRequired,
  onHideCallback: PropTypes.func.isRequired,
}

export const ConfirmationModal = ({ isShown, isLoading, onSubmitCallback, onHideCallback }) => {
  return (
    <Modal
      size="lg"
      show={isShown}
      onHide={onHideCallback}
    >
      <Modal.Header closeButton>
        <Modal.Title id="confirmation-modal">
          Are you sure that you want to remove the selected substances?
        </Modal.Title>
      </Modal.Header>

      <Modal.Footer>
        <button
          type="button"
          onClick={onHideCallback}
          className="btn btn-light btn-elevate"
        >
          No
        </button>
        <button
          type="submit"
          disabled={isLoading}
          onClick={onSubmitCallback}
          style={{ width: '100px' }}
          className="btn btn-primary btn-elevate"
        >
          Yes
          {isLoading && (<span className="ml-3 spinner spinner-white" />)}
        </button>
      </Modal.Footer>
    </Modal>
  )
}

ConfirmationModal.propTypes = propTypes;
