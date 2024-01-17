import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Modal } from "react-bootstrap";

import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulation/regulationActions";

import { UrlForm } from "./UrlForm";

const initUrl = {
  id: undefined,
  description: "",
  text: "",
};

export function UrlAddEditModal({
  showUrlAddModal,
  setShowUrlAddModal,
  selectedUrlId,
  regulationId,
}) {
  const dispatch = useDispatch();

  const { actionsLoading, regulationUrlForEdit } = useSelector(
    ({ regulation }) => ({
      actionsLoading: regulation.actionsLoading,
      regulationUrlForEdit: regulation.urlList?.find((url) => url.id === selectedUrlId),
    }),
  );

  const saveRegulationUrl = values => {
    const afterActionUpdate = () => {
      setShowUrlAddModal(false);
      dispatch(actions.fetchURLsList());
    };

    if (!selectedUrlId) {
      values.id = regulationId;
      dispatch(
        actions.createRegulationUrl({
          url: {
            ...values,
            description: values.description.toString("html"),
          },
          regulationId,
        })
      ).then(() => afterActionUpdate());
    } else {
      dispatch(actions.updateRegulationUrl({
        ...values,
        description: values.description.toString("html"),
      })).then(() => afterActionUpdate());
    }
  };

  return (
    <Modal
      size="lg"
      show={showUrlAddModal}
      onHide={() => setShowUrlAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedUrlId ? "Edit" : "Add"} Regulation Url
        </Modal.Title>
      </Modal.Header>

      <UrlForm
        setShowUrlAddModal={setShowUrlAddModal}
        saveRegulationUrl={saveRegulationUrl}
        url={regulationUrlForEdit || initUrl}
        actionsLoading={actionsLoading}
      />
    </Modal>
  );
}
