import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import React from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import RichTextEditor from "react-rte";

import { LinkForm as UrlForm } from "../useful-link-table/LinkForm";

const initUrl = {
  id: undefined,
  description: RichTextEditor.createEmptyValue(),
  text: "",
};

export function UrlAddEditModal({
  showUrlAddModal,
  setShowUrlAddModal,
  setEmptyMilestone,
  emptyMilestone,
  urlObject,
}) {
  const { actionsLoading } = useSelector(
    (state) => ({
      actionsLoading: state.regulation.actionsLoading,
    }),
    shallowEqual
  );

  const dispatch = useDispatch();

  const saveUrl = (values) => {
    const isDescriptionEmpty = values.description.toString("markdown").trim() === '\u200b';

    dispatch(
      actions.createMilestoneUrl({
        ...values,
        description: isDescriptionEmpty ? '' : values.description.toString("html"),
      }, setEmptyMilestone, emptyMilestone)
    ).then(() => {
      setShowUrlAddModal(false);
    });
  };

  const link = urlObject && {
    ...urlObject,
    description: RichTextEditor.createValueFromString(urlObject.description, "html")
  } || initUrl;

  return (
    <Modal
      size="lg"
      show={showUrlAddModal}
      onHide={() => setShowUrlAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">Add Url</Modal.Title>
      </Modal.Header>

      <UrlForm
        setShowLinkAddModal={setShowUrlAddModal}
        saveRegulatoryFrameworkLink={saveUrl}
        link={link}
      />
    </Modal>
  );
}
