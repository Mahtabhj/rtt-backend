import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import ReactSelect from 'react-select';
import { Modal } from "react-bootstrap";

import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulation/regulationActions";

export function UrlLinkUrlModal({
  setShowLinkUrlModal,
  showLinkUrlModal,
  regulationId,
  idsOfSelectedUrls,
}) {
  const dispatch = useDispatch();

  const { actionsLoading, regulationUrls = [] } = useSelector(({ regulation }) => ({
    actionsLoading: regulation.actionsLoading,
    regulationUrls: regulation.urlList,
  }));

  const [selectedUrls, setSelectedUrls] = useState([]);

  const saveLinkedUrls = () => {
    dispatch(actions.updateRegulationField({
      id: regulationId,
      urls: selectedUrls.map(({ id }) => id).concat(idsOfSelectedUrls),
    })).then(() => setShowLinkUrlModal(false))
  };

  useEffect(() => {
    if (!showLinkUrlModal) {
      setSelectedUrls([]);
    }
  }, [showLinkUrlModal]);

  const urlsListToShow = regulationUrls?.filter(({ id }) => !idsOfSelectedUrls.includes(id));

  const handleOnHide = () => setShowLinkUrlModal(false);

  return (
    <Modal
      size="lg"
      show={showLinkUrlModal}
      onHide={handleOnHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Link Url
        </Modal.Title>
      </Modal.Header>

      <Modal.Body>
        <ReactSelect
          isMulti
          options={urlsListToShow}
          getOptionLabel={(option) => option.text}
          getOptionValue={(option) => option.id}
          value={selectedUrls}
          onChange={setSelectedUrls}
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
          onClick={saveLinkedUrls}
          className="btn btn-primary btn-elevate"
        >
          Save
        </button>
      </Modal.Footer>
    </Modal>
  );
}
