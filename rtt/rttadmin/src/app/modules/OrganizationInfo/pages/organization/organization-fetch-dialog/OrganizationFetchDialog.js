import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useSelector } from "react-redux";
import { OrganizationStatusCssClasses } from "../OrganizationUIHelpers";
import { useOrganizationUIContext } from "../OrganizationUIContext";

const selectedOrganization = (entities, ids) => {
  const _organization = [];
  ids.forEach((id) => {
    const organization = entities.find((el) => el.id === id);
    if (organization) {
      _organization.push(organization);
    }
  });
  return _organization;
};

export function OrganizationFetchDialog({ show, onHide }) {
  // Organization UI Context
  const organizationUIContext = useOrganizationUIContext();
  const organizationUIProps = useMemo(() => {
    return {
      ids: organizationUIContext.ids,
      queryParams: organizationUIContext.queryParams,
    };
  }, [organizationUIContext]);

  // Organization Redux state
  const { organization } = useSelector(
    (state) => ({
      organization: selectedOrganization(state.organization.entities, organizationUIProps.ids),
    }),
    shallowEqual
  );

  // if there weren't selected ids we should close modal
  useEffect(() => {
    if (!organizationUIProps.ids || organizationUIProps.ids.length === 0) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [organizationUIProps.ids]);

  return (
    <Modal
      show={show}
      onHide={onHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Fetch selected elements
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div className="list-timeline list-timeline-skin-light padding-30">
          <div className="list-timeline-items">
            {organization.map((organization) => (
              <div className="list-timeline-item mb-3" key={organization.id}>
                <span className="list-timeline-text">
                  <span
                    className={`label label-lg label-light-${
                      OrganizationStatusCssClasses[organization.status]
                    } label-inline`}
                    style={{ width: "60px" }}
                  >
                    ID: {organization.id}
                  </span>{" "}
                  <span className="ml-5">
                    {organization.manufacture}, {organization.model}
                  </span>
                </span>
              </div>
            ))}
          </div>
        </div>
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
            onClick={onHide}
            className="btn btn-primary btn-elevate"
          >
            Ok
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
