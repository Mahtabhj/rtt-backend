/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-organization/organization/organizationActions";
import { useOrganizationUIContext } from "../OrganizationUIContext";

export function OrganizationDeleteDialog({ show, onHide }) {
  // Organization UI Context
  const organizationUIContext = useOrganizationUIContext();
  const organizationUIProps = useMemo(() => {
    return {
      ids: organizationUIContext.ids,
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

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  // if there weren't selected organization we should close modal
  useEffect(() => {
    if (!organizationUIProps.ids || organizationUIProps.ids.length === 0) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [organizationUIProps.ids]);

  const deleteOrganization = () => {
    // server request for deleting organization by seleted ids
    dispatch(actions.deleteOrganization(organizationUIProps.ids)).then(() => {
      // refresh list after deletion
      dispatch(actions.fetchOrganization(organizationUIProps.queryParams)).then(
        () => {
          // clear selections list
          organizationUIProps.setIds([]);
          // closing delete modal
          onHide();
        }
      );
    });
  };

  return (
    <Modal
      show={show}
      onHide={onHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Organization Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete selected organization?</span>
        )}
        {isLoading && <span>Organization are deleting...</span>}
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
            className="btn btn-primary btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
