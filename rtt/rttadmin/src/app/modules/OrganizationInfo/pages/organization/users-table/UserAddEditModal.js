import React, { useEffect } from "react";

import { Modal } from "react-bootstrap";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-organization/organization/organizationActions";
import { shallowEqual, useDispatch, useSelector } from "react-redux";

import { UserForm } from "./UserForm";

const initUser = {
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

export function UserAddEditModal({
  showUserAddModal,
  setShowUserAddModal,
  selectedUserId,
  organizationId,
}) {
  const dispatch = useDispatch();

  const { actionsLoading, organizationUserForEdit, success } = useSelector(
    (state) => ({
      actionsLoading: state.organization.actionsLoading,
      organizationUserForEdit: state.organization.organizationUserForEdit,
      success: state.organization.success,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.fetchOrganizationSelectedUser(selectedUserId));
  }, [selectedUserId, dispatch]);

  useEffect(() => {
    if (success === 'organization-user') {
      setShowUserAddModal(false)
    }
  }, [success]);

  const saveOrganizationUser = (values) => {
    if (!selectedUserId) {
      dispatch(
        actions.createOrganizationUser({
          ...values,
          organization: organizationId,
          username: values.email,
        })
      )
    } else {
      dispatch(actions.updateOrganizationUser(values))
    }
  };

  return (
    <Modal
      size="lg"
      show={showUserAddModal}
      onHide={() => setShowUserAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedUserId ? "Edit" : "Add"} Organization User
        </Modal.Title>
      </Modal.Header>

      <UserForm
        organizationId={organizationId}
        setShowUserAddModal={setShowUserAddModal}
        saveOrganizationUser={saveOrganizationUser}
        user={organizationUserForEdit || initUser}
      />
    </Modal>
  );
}
