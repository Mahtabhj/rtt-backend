import React from "react";
import { OverlayTrigger, Tooltip } from "react-bootstrap";
import SVG from "react-inlinesvg";
import { toAbsoluteUrl } from "../../../../../../../_metronic/_helpers";

export const ActionsColumnFormatter = (
  cellContent,
  row,
  rowIndex,
  { openEditImpactAssessmentPage, openDeleteImpactAssessmentDialog }
) => (
  <>
    <> </>

    <OverlayTrigger
      overlay={<Tooltip id="impactAssessment-edit-tooltip">Edit</Tooltip>}
    >
      <button
        className="btn btn-icon btn-light btn-hover-primary btn-sm mx-3"
        onClick={() => openEditImpactAssessmentPage(row.id)}
      >
        <span className="svg-icon svg-icon-md svg-icon-primary">
          <SVG
            src={toAbsoluteUrl(process.env.REACT_APP_STATIC_PATH + "/svg/icons/Communication/Write.svg")}
          />
        </span>
      </button>
    </OverlayTrigger>

    <> </>

    <OverlayTrigger
      overlay={<Tooltip id="organization-delete-tooltip">Delete</Tooltip>}
    >
      <button 
        className="btn btn-icon btn-light btn-hover-danger btn-sm"
        onClick={() => openDeleteImpactAssessmentDialog(row.id)}
      >
        <span className="svg-icon svg-icon-md svg-icon-danger">
          <SVG src={toAbsoluteUrl(process.env.REACT_APP_STATIC_PATH + "/svg/icons/General/Trash.svg")} />
        </span>
      </button>
    </OverlayTrigger>
  </>
);
