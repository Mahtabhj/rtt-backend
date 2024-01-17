import React, { useMemo } from "react";
import { useNewsUIContext } from "../NewsUIContext";

export function NewsGrouping() {
  // News UI Context
  const newsUIContext = useNewsUIContext();
  const newsUIProps = useMemo(() => {
    return {
      ids: newsUIContext.ids,
      setIds: newsUIContext.setIds,
      openDeleteNewsDialog: newsUIContext.openDeleteNewsDialog,
      openFetchNewsDialog: newsUIContext.openFetchNewsDialog,
      openUpdateNewsStatusDialog:
        newsUIContext.openUpdateNewsStatusDialog,
    };
  }, [newsUIContext]);

  return (
    <div className="form">
      <div className="row align-items-center form-group-actions margin-top-20 margin-bottom-20">
        <div className="col-xl-12">
          <div className="form-group form-group-inline">
            <div className="form-label form-label-no-wrap">
              <label className="-font-bold font-danger-">
                <span>
                  Selected records count: <b>{newsUIProps.ids.length}</b>
                </span>
              </label>
            </div>
            <div>

              <button
                type="button"
                className="btn btn-danger font-weight-bolder font-size-sm"
                onClick={newsUIProps.openDeleteNewsDialog}
              >
                <i className="fa fa-trash"></i> Delete All
              </button> &nbsp;

              <button
                type="button"
                className="btn btn-light-primary font-weight-bolder font-size-sm"
                onClick={newsUIProps.openFetchNewsDialog}
              >
                <i className="fa fa-stream"></i> Fetch Selected
              </button> &nbsp;

              <button
                type="button"
                className="btn btn-light-primary font-weight-bolder font-size-sm"
                onClick={newsUIProps.openUpdateNewsStatusDialog}
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
