import React, { useEffect } from "react";

import { Modal } from "react-bootstrap";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/organization/organizationActions";
import { shallowEqual, useDispatch, useSelector } from "react-redux";

import { RegulationForm } from "./RegulationForm";

const initRegulation = {
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

export function RegulationAddEditModal({
  showRegulationAddModal,
  setShowRegulationAddModal,
  selectedRegulationId,
  organizationId,
}) {
  const dispatch = useDispatch();

  const { actionsLoading, organizationRegulationForEdit } = useSelector(
    (state) => ({
      actionsLoading: state.organization.actionsLoading,
      organizationRegulationForEdit:
        state.organization.organizationRegulationForEdit,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.fetchOrganizationSelectedRegulation(selectedRegulationId));
  }, [selectedRegulationId, dispatch]);

  const saveOrganizationRegulation = (values) => {
    if (!selectedRegulationId) {
      dispatch(
        actions.createOrganizationRegulation({
          ...values,
          organization: organizationId,
          username: values.email,
        })
      ).then(() => setShowRegulationAddModal(false));
    } else {
      dispatch(actions.updateOrganizationRegulation(values)).then(() =>
        setShowRegulationAddModal(false)
      );
    }
  };

  return (
    <Modal
      size="lg"
      show={showRegulationAddModal}
      onHide={() => setShowRegulationAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedRegulationId ? "Edit" : "Add"} Organization Regulation
        </Modal.Title>
      </Modal.Header>

      <RegulationForm
        setShowRegulationAddModal={setShowRegulationAddModal}
        saveOrganizationRegulation={saveOrganizationRegulation}
        regulation={organizationRegulationForEdit || initRegulation}
      />
    </Modal>
  );
}
