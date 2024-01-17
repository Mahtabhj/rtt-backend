/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid */
import React from "react";
import { OverlayTrigger, Tooltip } from "react-bootstrap";
import SVG from "react-inlinesvg";

import { toAbsoluteUrl } from "@metronic-helpers";

export const ActionsColumnFormatter = (
  cellContent,
  row,
  rowIndex,
  { openEditImpactAssessmentPage }
) => (
  <OverlayTrigger overlay={<Tooltip id="impactAssessment-edit-tooltip">Expand</Tooltip>}>
    <a
      className="btn btn-icon btn-light btn-hover-primary btn-sm mx-3"
      onClick={() =>{
        openEditImpactAssessmentPage(row.id-1);
      } }
    >
        <span className="svg-icon svg-icon-md svg-icon-primary">
          <SVG
            src={toAbsoluteUrl(process.env.REACT_APP_STATIC_PATH + "/svg/icons/Files/File-plus.svg")}
          />
        </span>
    </a>
  </OverlayTrigger>
);
