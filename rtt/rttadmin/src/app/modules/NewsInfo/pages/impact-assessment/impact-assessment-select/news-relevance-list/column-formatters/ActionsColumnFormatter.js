import React from "react";
import { OverlayTrigger, Tooltip } from "react-bootstrap";
import SVG from "react-inlinesvg";

import { toAbsoluteUrl } from "@metronic-helpers";

export const ActionsColumnFormatter = (
  cellContent,
  row,
  rowIndex,
  { openEditNewsRelevancePage }
) => {
  const handleOpenEditRelevancePage = (e) => {
    e.currentTarget.blur(); // fast solution to make button unfocused after closing modal
    openEditNewsRelevancePage(row.id);
  };

  return (
    <OverlayTrigger
      overlay={<Tooltip id="newsRelevance-edit-tooltip">Use main app to edit completed relevance</Tooltip>}
    >
      <div style={{marginLeft: 'auto', width: 'min-content'}}>
        <button
          className="btn btn-icon btn-light btn-hover-primary btn-sm mx-3"
          onClick={handleOpenEditRelevancePage}
          disabled
        >
          <span className="svg-icon svg-icon-md svg-icon-primary">
            <SVG
              src={toAbsoluteUrl(process.env.REACT_APP_STATIC_PATH + "/svg/icons/Communication/Write.svg")}
            />
          </span>
        </button>
      </div>
    </OverlayTrigger>
  )
};
