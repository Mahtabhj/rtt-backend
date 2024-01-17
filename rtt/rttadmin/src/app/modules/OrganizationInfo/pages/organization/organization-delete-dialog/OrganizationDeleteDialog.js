/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-organization/organization/organizationActions";
import { useOrganizationUIContext } from "../OrganizationUIContext";

export function OrganizationDeleteDialog({ id, show, onHide }) {
  // Organization UI Context
  const organizationUIContext = useOrganizationUIContext();
  const organizationUIProps = useMemo(() => {
    return {
      setIds: organizationUIContext.setIds,
      queryParams: organizationUIContext.queryParams,
    };
  }, [organizationUIContext]);

  // Organization Redux state
  const dispatch = useDispatch();
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.organization.actionsLoading }),
    shallowEqual
  );

  // if !id we should close modal
  useEffect(() => {
    if (!id) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  const deleteOrganization = () => {
    // server request for deleting organization by id
    dispatch(actions.deleteOrganization(id)).then(() => {
      // refresh list after deletion
      dispatch(actions.fetchOrganizationList(organizationUIProps.queryParams));
      // clear selections list
      organizationUIProps.setIds([]);
      // closing delete modal
      onHide();
    });
  };

  return (
    <Modal
      show={show}
      onHide={onHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Organization Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this organization?</span>
        )}
        {isLoading && <span>Organization is deleting...</span>}
      </Modal.Body>
      <Modal.Footer>
        <div>
          <button
            type="button"
            onClick={onHide}
            className="btn btn-light btn-elevate"
          >
            Cancel
          </button>
          <> </>
          <button
            type="button"
            onClick={deleteOrganization}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
