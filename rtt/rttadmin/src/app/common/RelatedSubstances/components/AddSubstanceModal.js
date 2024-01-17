import React, { useState } from "react";
import { Modal } from "react-bootstrap";
import PropTypes from "prop-types";

import { AddSubstanceForm } from "./AddSubstanceForm";

const propTypes = {
  updateCallback: PropTypes.func.isRequired,
}

export const AddSubstanceModal = ({ updateCallback }) => {
  const [showAddModal, setShowAddModal] = useState(false);

  const handleShowModal = () => setShowAddModal(prevState => !prevState);

  return (
    <>
      <button
        type="button"
        className="btn btn-primary"
        onClick={handleShowModal}
      >
        Add Substance
      </button>

      {showAddModal && (
        <Modal
          size="lg"
          show={showAddModal}
          onHide={() => {
            setShowAddModal(false)
          }}
        >
          <Modal.Header closeButton>
            <Modal.Title id="example-modal-sizes-title-lg">
              Add Substance
            </Modal.Title>
          </Modal.Header>

          <AddSubstanceForm onClose={handleShowModal} updateCallback={updateCallback} />
        </Modal>
      )}
    </>
  )
}

AddSubstanceModal.propTypes = propTypes;
