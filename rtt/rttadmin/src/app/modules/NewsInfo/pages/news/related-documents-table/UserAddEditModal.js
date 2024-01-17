import React, { useEffect } from "react";

import { Modal } from "react-bootstrap";
import { ModalProgressBar } from "../../../../../../_metronic/_partials/controls";
import * as actions from "../../../_redux/organization/organizationActions";
import { shallowEqual, useDispatch, useSelector } from "react-redux";

import { NewsForm } from "./NewsForm";

const initNews = {
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

export function NewsAddEditModal({
  showNewsAddModal,
  setShowNewsAddModal,
  selectedNewsId,
  organizationId,
}) {
  const dispatch = useDispatch();

  const { actionsLoading, organizationNewsForEdit } = useSelector(
    (state) => ({
      actionsLoading: state.organization.actionsLoading,
      organizationNewsForEdit:
        state.organization.organizationNewsForEdit,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.fetchOrganizationSelectedNews(selectedNewsId));
  }, [selectedNewsId, dispatch]);

  const saveOrganizationNews = (values) => {
    if (!selectedNewsId) {
      dispatch(
        actions.createOrganizationNews({
          ...values,
          organization: organizationId,
          username: values.email,
        })
      ).then(() => setShowNewsAddModal(false));
    } else {
      dispatch(actions.updateOrganizationNews(values)).then(() =>
        setShowNewsAddModal(false)
      );
    }
  };

  return (
    <Modal
      size="lg"
      show={showNewsAddModal}
      onHide={() => setShowNewsAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedNewsId ? "Edit" : "Add"} Organization News
        </Modal.Title>
      </Modal.Header>

      <NewsForm
        setShowNewsAddModal={setShowNewsAddModal}
        saveOrganizationNews={saveOrganizationNews}
        news={organizationNewsForEdit || initNews}
      />
    </Modal>
  );
}
