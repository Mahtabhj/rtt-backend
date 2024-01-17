/* eslint-disable no-restricted-imports */
import React, { useEffect } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-organization/organization/organizationActions";

export function SubscriptionDeleteDialog({
  selectedSubscriptionIdDelete,
  showSubscriptionDeleteModal,
  setShowSubscriptionDeleteModal,
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
    if (!selectedSubscriptionIdDelete) {
      setShowSubscriptionDeleteModal(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedSubscriptionIdDelete, dispatch]);

  // looking for loading/dispatch

  const deleteSubscription = () => {
    // server request for deleting organization by id
    dispatch(
      actions.deleteOrganizationSubscription(selectedSubscriptionIdDelete)
    ).then(() => {
      dispatch(actions.fetchOrganizationSubscriptionList(organizationId));
      setShowSubscriptionDeleteModal(false);
    });
  };

  return (
    <Modal
      show={showSubscriptionDeleteModal}
      onHide={() => setShowSubscriptionDeleteModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Organization Subscription Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this subscription?</span>
        )}
        {isLoading && <span>Organization is deleting...</span>}
      </Modal.Body>
      <Modal.Footer>
        <div>
          <button
            type="button"
            onClick={() => setShowSubscriptionDeleteModal(false)}
            className="btn btn-light btn-elevate"
          >
            Cancel
          </button>
          <> </>
          <button
            type="button"
            onClick={deleteSubscription}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
