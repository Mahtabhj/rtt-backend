import React from "react";

import { Modal } from "react-bootstrap";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-organization/organization/organizationActions";
import { shallowEqual, useDispatch, useSelector } from "react-redux";

import { PasswordChangeForm } from "./PasswordChange";

export function UserPasswordChangeModal({
  showUserPasswordChangeModal,
  setShowUserPasswordChangeModal,
  selectedUserId,
}) {
  const dispatch = useDispatch();
  const { actionsLoading } = useSelector(
    (state) => ({
      actionsLoading: state.organization.actionsLoading,
    }),
    shallowEqual
  );

  const saveNewPassword = (values) => {
    const data = { ...values, id: selectedUserId };
    dispatch(actions.chnageUserPassword(data)).then(() => {
      setShowUserPasswordChangeModal(false);
    });
  };

  return (
    <Modal
      size="lg"
      show={showUserPasswordChangeModal}
      onHide={() => setShowUserPasswordChangeModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Organization User's Password Change
        </Modal.Title>
      </Modal.Header>

      <PasswordChangeForm
        setShowUserPasswordChangeModal={setShowUserPasswordChangeModal}
        saveNewPassword={saveNewPassword}
      />
    </Modal>
  );
}
