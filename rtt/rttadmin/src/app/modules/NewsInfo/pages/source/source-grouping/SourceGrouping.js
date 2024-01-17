import React, { useMemo } from "react";
import { useSourceUIContext } from "../SourceUIContext";

export function SourceGrouping() {
  // Source UI Context
  const sourceUIContext = useSourceUIContext();
  const sourceUIProps = useMemo(() => {
    return {
      ids: sourceUIContext.ids,
      setIds: sourceUIContext.setIds,
      openDeleteSourceDialog: sourceUIContext.openDeleteSourceDialog,
      openFetchSourceDialog: sourceUIContext.openFetchSourceDialog,
      openUpdateSourceStatusDialog:
        sourceUIContext.openUpdateSourceStatusDialog,
    };
  }, [sourceUIContext]);

  return (
    <div className="form">
      <div className="row align-items-center form-group-actions margin-top-20 margin-bottom-20">
        <div className="col-xl-12">
          <div className="form-group form-group-inline">
            <div className="form-label form-label-no-wrap">
              <label className="-font-bold font-danger-">
                <span>
                  Selected records count: <b>{sourceUIProps.ids.length}</b>
                </span>
              </label>
            </div>
            <div>
              <button
                type="button"
                className="btn btn-danger font-weight-bolder font-size-sm"
                onClick={sourceUIProps.openDeleteSourceDialog}
              >
                <i className="fa fa-trash"></i> Delete All
              </button>{" "}
              &nbsp;
              <button
                type="button"
                className="btn btn-light-primary font-weight-bolder font-size-sm"
                onClick={sourceUIProps.openFetchSourceDialog}
              >
                <i className="fa fa-stream"></i> Fetch Selected
              </button>{" "}
              &nbsp;
              <button
                type="button"
                className="btn btn-light-primary font-weight-bolder font-size-sm"
                onClick={sourceUIProps.openUpdateSourceStatusDialog}
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
