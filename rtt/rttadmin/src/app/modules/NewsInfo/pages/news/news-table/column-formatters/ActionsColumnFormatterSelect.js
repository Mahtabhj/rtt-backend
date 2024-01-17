/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid */
import React from "react";
import { OverlayTrigger, Tooltip } from "react-bootstrap";
import SVG from "react-inlinesvg";

import { toAbsoluteUrl } from "@metronic-helpers";

export const ActionsColumnFormatterSelect = (
  cellContent,
  row,
  rowIndex,
  { openSelectNewsPage, dischargeNews }
) => (
  <>
    <OverlayTrigger
      overlay={<Tooltip id="news-select-tooltip">Select news</Tooltip>}
    >
      <a
        className="btn btn-icon btn-light btn-hover-primary btn-sm mx-3"
        onClick={() => openSelectNewsPage(row.id)}
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

    <OverlayTrigger
      overlay={<Tooltip id="news-delete-tooltip">Discharge news</Tooltip>}
    >
      <a
        className="btn btn-icon btn-light btn-hover-danger btn-sm"
        onClick={() => dischargeNews(row.id)}
      >
        <span className="svg-icon svg-icon-md svg-icon-danger">
          <SVG
            src={toAbsoluteUrl(
              process.env.REACT_APP_STATIC_PATH + "/svg/icons/Navigation/Arrow-from-bottom.svg"
            )}
          />
        </span>
      </a>
    </OverlayTrigger>
  </>
);
