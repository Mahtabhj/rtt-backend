import React, { useEffect } from "react";

import { Modal } from "react-bootstrap";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulatoryFramework/organization/organizationActions";
import { shallowEqual, useDispatch, useSelector } from "react-redux";

import { RegulatoryFrameworkForm } from "./RegulatoryFrameworkForm";

const initRegulatoryFramework = {
  id: undefined,
  first_name: "",
  last_name: "",
  email: "",
  username: "",
  password: "",
  country: "",
  city: "",
  is_admin: "True",
  is_active: true,
};

export function RegulatoryFrameworkAddEditModal({
  showRegulatoryFrameworkAddModal,
  setShowRegulatoryFrameworkAddModal,
  selectedRegulatoryFrameworkId,
  organizationId,
}) {
  const dispatch = useDispatch();

  const { actionsLoading, organizationRegulatoryFrameworkForEdit } = useSelector(
    (state) => ({
      actionsLoading: state.organization.actionsLoading,
      organizationRegulatoryFrameworkForEdit:
        state.organization.organizationRegulatoryFrameworkForEdit,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.fetchOrganizationSelectedRegulatoryFramework(selectedRegulatoryFrameworkId));
  }, [selectedRegulatoryFrameworkId, dispatch]);

  const saveOrganizationRegulatoryFramework = (values) => {
    if (!selectedRegulatoryFrameworkId) {
      dispatch(
        actions.createOrganizationRegulatoryFramework({
          ...values,
          organization: organizationId,
          username: values.email,
        })
      ).then(() => setShowRegulatoryFrameworkAddModal(false));
    } else {
      dispatch(actions.updateOrganizationRegulatoryFramework(values)).then(() =>
        setShowRegulatoryFrameworkAddModal(false)
      );
    }
  };

  return (
    <Modal
      size="lg"
      show={showRegulatoryFrameworkAddModal}
      onHide={() => setShowRegulatoryFrameworkAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedRegulatoryFrameworkId ? "Edit" : "Add"} Organization RegulatoryFramework
        </Modal.Title>
      </Modal.Header>

      <RegulatoryFrameworkForm
        setShowRegulatoryFrameworkAddModal={setShowRegulatoryFrameworkAddModal}
        saveOrganizationRegulatoryFramework={saveOrganizationRegulatoryFramework}
        regulatoryFramework={organizationRegulatoryFrameworkForEdit || initRegulatoryFramework}
      />
    </Modal>
  );
}
