import React from "react";
import { OverlayTrigger, Tooltip } from "react-bootstrap";
import SVG from "react-inlinesvg";
import { toAbsoluteUrl } from "@metronic-helpers";

export const ActionsColumnFormatter = (
  cellContent,
  row,
  rowIndex,
  {
    openSelectImpactAssessmentPage,
  }
) => (
  <>
    <OverlayTrigger
      overlay={
        <Tooltip id="impactAssessment-edit-tooltip">
          Select impact assessment
        </Tooltip>
      }
    >
      <a
        className="btn btn-icon btn-light btn-hover-primary btn-sm mx-3"
        onClick={() => {
          openSelectImpactAssessmentPage(row.id);
        }}
      >
        <span className="svg-icon svg-icon-md svg-icon-primary">
          <SVG
            src={toAbsoluteUrl(
              process.env.REACT_APP_STATIC_PATH +
              "/svg/icons/Communication/Clipboard-check.svg"
            )}
          />
        </span>
      </a>
    </OverlayTrigger>
  </>
);
