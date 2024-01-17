import React from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import RichTextEditor from "react-rte";
import { Modal } from "react-bootstrap";

import { ModalProgressBar } from "@metronic-partials/controls";
import {
  createMilestoneUrl as createRegulationMilestoneUrl,
  updateMilestoneUrl as updateRegulationMilestoneUrl
} from "@redux-regulation/regulation/regulationActions";
import {
  createMilestoneUrl as createRegulatoryFrameworkMilestoneUrl,
  updateMilestoneUrl as updateRegulatoryFrameworkMilestoneUrl
} from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";

import { UrlForm } from "./UrlForm";

const urlActions = {
  regulation: {
    createMilestoneUrl: createRegulationMilestoneUrl,
    updateMilestoneUrl: updateRegulationMilestoneUrl,
  },
  regulatoryFramework: {
    createMilestoneUrl: createRegulatoryFrameworkMilestoneUrl,
    updateMilestoneUrl: updateRegulatoryFrameworkMilestoneUrl,
  }
};

const initUrl = {
  id: undefined,
  description: RichTextEditor.createEmptyValue(),
  text: "",
};

export function UrlAddEditModal({
  type,
  showUrlAddModal,
  setShowUrlAddModal,
  urlObject,
  setUpdatedUrl
}) {
  const dispatch = useDispatch();
  const { actionsLoading } = useSelector(
    (state) => ({
      actionsLoading: state[type].actionsLoading,
    }),
    shallowEqual
  );

  const saveUrl = (values) => {
    const isDescriptionEmpty = values.description.toString("markdown").trim() === '\u200b';
    const description = isDescriptionEmpty ? '' : values.description.toString("html");
    const valuesForRequest = { ...values, description: description };

    if (values.id) {
      dispatch(
        urlActions[type].updateMilestoneUrl(valuesForRequest)
      ).then(() => {
        setShowUrlAddModal(false);
        setUpdatedUrl(valuesForRequest);
      });
    } else {
      dispatch(
        urlActions[type].createMilestoneUrl(valuesForRequest)
      ).then(() => {
        setShowUrlAddModal(false);
      });
    }
  };

  const url = urlObject && {
    ...urlObject,
    description: RichTextEditor.createValueFromString(urlObject.description, "html")
  } || initUrl;

  const handleOnHide = () => setShowUrlAddModal(false);

  return (
    <Modal
      size="lg"
      show={showUrlAddModal}
      onHide={handleOnHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">Add Url</Modal.Title>
      </Modal.Header>

      <UrlForm
        setShowUrlAddModal={setShowUrlAddModal}
        saveUrl={saveUrl}
        url={url}
      />
    </Modal>
  );
}
