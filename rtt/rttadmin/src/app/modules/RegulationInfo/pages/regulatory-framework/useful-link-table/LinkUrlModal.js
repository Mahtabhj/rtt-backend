import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import React, { useEffect, useState } from "react";
import { Modal } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import ReactSelect from 'react-select';

export function LinkUrlModal({
  setShowLinkUrlModal,
  showLinkUrlModal,
  regulatoryFrameworkId,
  idsOfSelectedUrls,
}) {
  const dispatch = useDispatch();

  const { urlList, actionsLoading } = useSelector(({ regulatoryFramework }) => ({
    urlList: regulatoryFramework.urls,
    actionsLoading: regulatoryFramework.actionsLoading
  }));

  const [selectedUrls, setSelectedUrls] = useState([]);

  const saveLinkedUrls = () => {
    dispatch(actions.updateRegulatoryFrameworkField({
      id: regulatoryFrameworkId,
      urls: selectedUrls.map((url) => url.id).concat(idsOfSelectedUrls),
    })).then(() => {
      setShowLinkUrlModal(false);
    })
  };

  useEffect(() => {
    if (!showLinkUrlModal) {
      setSelectedUrls([]);
    }
  }, [showLinkUrlModal]);

  const urlsListToShow = urlList?.filter((url) => !idsOfSelectedUrls.includes(url.id)) || [];

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
