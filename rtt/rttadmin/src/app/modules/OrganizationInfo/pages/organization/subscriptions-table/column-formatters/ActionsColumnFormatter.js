/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid */
import React from "react";
import { OverlayTrigger, Tooltip } from "react-bootstrap";
import SVG from "react-inlinesvg";
import { toAbsoluteUrl } from "@metronic-helpers";

export const ActionsColumnFormatter = (
  cellContent,
  row,
  rowIndex,
  {
    openEditOrganizationSubscriptionPage,
    openSelectOrganizationPage,
    openDeleteOrganizationSubscriptionDialog,
  }
) => (
  <>

    <> </>

    <OverlayTrigger
      overlay={
        <Tooltip id="organization-edit-tooltip">Edit subscription</Tooltip>
      }
    >
      <a
        className="btn btn-icon btn-light btn-hover-primary btn-sm mx-3"
        onClick={() => openEditOrganizationSubscriptionPage(row.id)}
      >
        <span className="svg-icon svg-icon-md svg-icon-primary">
          <SVG
            src={toAbsoluteUrl(
              process.env.REACT_APP_STATIC_PATH +
                "/svg/icons/Communication/Write.svg"
            )}
          />
        </span>
      </a>
    </OverlayTrigger>

    <> </>

    <OverlayTrigger
      overlay={
        <Tooltip id="organization-delete-tooltip">Delete subscription</Tooltip>
      }
    >
      <a
        className="btn btn-icon btn-light btn-hover-danger btn-sm"
        onClick={() => openDeleteOrganizationSubscriptionDialog(row.id)}
      >
        <span className="svg-icon svg-icon-md svg-icon-danger">
          <SVG
            src={toAbsoluteUrl(
              process.env.REACT_APP_STATIC_PATH + "/svg/icons/General/Trash.svg"
            )}
          />
        </span>
      </a>
    </OverlayTrigger>
  </>
);
