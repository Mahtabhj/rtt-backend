import React, { useMemo } from "react";
import { useOrganizationUIContext } from "../OrganizationUIContext";

export function OrganizationGrouping() {
  // Organization UI Context
  const organizationUIContext = useOrganizationUIContext();
  const organizationUIProps = useMemo(() => {
    return {
      ids: organizationUIContext.ids,
      setIds: organizationUIContext.setIds,
      openDeleteOrganizationDialog: organizationUIContext.openDeleteOrganizationDialog,
      openFetchOrganizationDialog: organizationUIContext.openFetchOrganizationDialog,
      openUpdateOrganizationStatusDialog:
        organizationUIContext.openUpdateOrganizationStatusDialog,
    };
  }, [organizationUIContext]);

  return (
    <div className="form">
      <div className="row align-items-center form-group-actions margin-top-20 margin-bottom-20">
        <div className="col-xl-12">
          <div className="form-group form-group-inline">
            <div className="form-label form-label-no-wrap">
              <label className="-font-bold font-danger-">
                <span>
                  Selected records count: <b>{organizationUIProps.ids.length}</b>
                </span>
              </label>
            </div>
            <div>

              <button
                type="button"
                className="btn btn-danger font-weight-bolder font-size-sm"
                onClick={organizationUIProps.openDeleteOrganizationDialog}
              >
                <i className="fa fa-trash"></i> Delete All
              </button> &nbsp;

              <button
                type="button"
                className="btn btn-light-primary font-weight-bolder font-size-sm"
                onClick={organizationUIProps.openFetchOrganizationDialog}
              >
                <i className="fa fa-stream"></i> Fetch Selected
              </button> &nbsp;

              <button
                type="button"
                className="btn btn-light-primary font-weight-bolder font-size-sm"
                onClick={organizationUIProps.openUpdateOrganizationStatusDialog}
              >
                <i className="fa fa-sync-alt"></i> Update Status
              </button>
              
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
