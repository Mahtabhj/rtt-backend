/* eslint-disable no-restricted-imports */
import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-organization/organization/organizationActions";

export function UserDeleteDialog({
  selectedUserIdDelete,
  showUserDeleteModal,
  setShowUserDeleteModal,
  organizationId,
}) {
  // Organization Redux state
  const dispatch = useDispatch();

  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.organization.actionsLoading }),
    shallowEqual
  );

  // if !id we should close modal
  useEffect(() => {
    if (!selectedUserIdDelete) {
      setShowUserDeleteModal(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedUserIdDelete, dispatch]);

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  const deleteUser = () => {
    // server request for deleting organization by id
    dispatch(actions.deleteOrganizationUser(selectedUserIdDelete)).then(() => {
      dispatch(actions.fetchOrganizationUserList(organizationId));
      setShowUserDeleteModal(false);
    });
  };

  return (
    <Modal
      show={showUserDeleteModal}
      onHide={() => setShowUserDeleteModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Organization User Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this user?</span>
        )}
        {isLoading && <span>Organization is deleting...</span>}
      </Modal.Body>
      <Modal.Footer>
        <div>
          <button
            type="button"
            onClick={() => setShowUserDeleteModal(false)}
            className="btn btn-light btn-elevate"
          >
            Cancel
          </button>
          <> </>
          <button
            type="button"
            onClick={deleteUser}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
