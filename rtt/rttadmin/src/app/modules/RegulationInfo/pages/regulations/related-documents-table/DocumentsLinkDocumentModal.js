import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulation/regulationActions";
import React, { useState, useEffect } from "react";
import { Modal } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import ReactSelect from 'react-select';

export function DocumentsLinkDocumentModal({
  setShowLinkDocumentModal,
  showLinkDocumentModal,
  regulationId,
  idsOfSelectedDocuments,
}) {
  const dispatch = useDispatch();

  const { actionsLoading, documents = [] } = useSelector(
    (state) => ({
      actionsLoading: state.regulation.actionsLoading,
      documents: state.regulation.documentList,
    }),
  );

  const [selectedDocuments, setSelectedDocuments] = useState([]);

  const saveLinkedDocuments = () => {
    dispatch(actions.updateRegulationField({
      id: regulationId,
      documents: selectedDocuments.map(({ id }) => id).concat(idsOfSelectedDocuments),
    })).then(() => setShowLinkDocumentModal(false))
  };

  useEffect(() => {
    if (!showLinkDocumentModal) {
      setSelectedDocuments([]);
    }
  }, [showLinkDocumentModal]);

  const documentsListToShow = documents.filter(({ id }) => !idsOfSelectedDocuments.includes(id));

  const handleOnHide = () => setShowLinkDocumentModal(false);

  return (
    <Modal
      size="lg"
      show={showLinkDocumentModal}
      onHide={handleOnHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Link Attachment
        </Modal.Title>
      </Modal.Header>

      <Modal.Body>
        <ReactSelect
          isMulti
          options={documentsListToShow}
          getOptionLabel={(option) => option.title}
          getOptionValue={(option) => option.id}
          value={selectedDocuments}
          onChange={setSelectedDocuments}
        />
      </Modal.Body>

      <Modal.Footer>
        <button
          type="button"
          onClick={handleOnHide}
          className="btn btn-light btn-elevate"
          disabled={actionsLoading}
        >
          Cancel
        </button>

        <button
          type="submit"
          onClick={saveLinkedDocuments}
          className="btn btn-primary btn-elevate"
        >
          Save
        </button>
      </Modal.Footer>
    </Modal>
  );
}
