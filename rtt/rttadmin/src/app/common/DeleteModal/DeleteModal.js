import React from "react";
import { Modal } from "react-bootstrap";
import PropTypes from "prop-types";

import { ModalProgressBar } from "@metronic-partials/controls";

import { DateInput } from "@common";

const noop = () => {};

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  itemsCount: PropTypes.number,
  date: PropTypes.string,
  setDate: PropTypes.func,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  title: PropTypes.string,
  actionButton: PropTypes.string,
}

const defaultProps = {
  itemsCount: null,
  date: null,
  setDate: noop,
  title: '',
  actionButton: 'Delete',
  size: 'lg',
}

export const DeleteModal = ({ title, isModalShown, itemsCount, date, setDate, onClose, onSubmit, actionsLoading, actionButton, size }) => {

  const handleOnChangeDate = ({ value }) => setDate(value ? value.toISOString() : '');

  return (
    <Modal
      size={size}
      show={isModalShown}
      onHide={onClose}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}

      <Modal.Header>
        <Modal.Title id="example-modal-sizes-title-lg">
          {title || `Are you sure you want to set ${itemsCount} records as deleted`}
        </Modal.Title>
      </Modal.Header>

      {typeof date === 'string' && (
        <Modal.Body className="overlay overlay-block cursor-default">
          <div className="form-group row">
            <div className="col-lg-3">
              <label>Updated on</label>
              <DateInput
                  id="modified"
                  value={date}
                  onChangeCallback={handleOnChangeDate}
              />
            </div>
          </div>
        </Modal.Body>
      )}

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
          className="btn btn-danger btn-elevate"
          style={{ minWidth: "120px" }}
        >
          {actionButton}
          {actionsLoading && (<span className="ml-3 spinner spinner-white" />)}
        </button>
      </Modal.Footer>
    </Modal>
  );
}

DeleteModal.propTypes = propTypes;
DeleteModal.defaultProps = defaultProps;
