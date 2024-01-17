import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import React from "react";
import { Modal } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { LinkForm } from "./LinkForm";

const initLink = {
  id: undefined,
  description: "",
  text: "",
};

export function LinkAddEditModal({
  showLinkAddModal,
  setShowLinkAddModal,
  selectedLinkId,
  regulatoryFrameworkId,
}) {
  const dispatch = useDispatch();

  const { actionsLoading, regulatoryFrameworkLinkForEdit } = useSelector(
    ({ regulatoryFramework }) => ({
      actionsLoading: regulatoryFramework.actionsLoading,
      regulatoryFrameworkLinkForEdit: regulatoryFramework.regulatoryFrameworkForEdit?.urls?.find(
        (link) => link.id === selectedLinkId
      ),
    }),
  );

  const saveRegulatoryFrameworkLink = (values) => {
    const afterActionUpdate = () => {
      setShowLinkAddModal(false);
      dispatch(actions.fetchLinkList());
    };

    if (!selectedLinkId) {
      values.id = regulatoryFrameworkId;
      dispatch(
        actions.createRegulatoryFrameworkLink({
          ...values,
          link: regulatoryFrameworkId,
        })
      ).then(() => afterActionUpdate());
    } else {
      dispatch(actions.updateRegulatoryFrameworkLink(values)).then(() => afterActionUpdate());
    }
  };

  const handleOnHide = () => setShowLinkAddModal(false);

  return (
    <Modal
      size="lg"
      show={showLinkAddModal}
      onHide={handleOnHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedLinkId ? "Edit" : "Add"} Regulatory Framework Link
        </Modal.Title>
      </Modal.Header>

      <LinkForm
        setShowLinkAddModal={setShowLinkAddModal}
        saveRegulatoryFrameworkLink={saveRegulatoryFrameworkLink}
        link={regulatoryFrameworkLinkForEdit || initLink}
        actionsLoading={actionsLoading}
      />
    </Modal>
  );
}
