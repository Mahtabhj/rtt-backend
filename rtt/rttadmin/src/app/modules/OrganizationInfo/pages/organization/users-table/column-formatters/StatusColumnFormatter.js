import React from "react";
import {
  OrganizationStatusCssClasses,
  OrganizationStatusTitles,
} from "../../OrganizationUIHelpers";

export const StatusColumnFormatter = (cellContent, row) => {
  let index = cellContent ? 0 : 1;
  return (
    <span
      className={`label label-lg label-light-${OrganizationStatusCssClasses[index]} label-inline`}
    >
      {OrganizationStatusTitles[index]}
    </span>
  );
};
