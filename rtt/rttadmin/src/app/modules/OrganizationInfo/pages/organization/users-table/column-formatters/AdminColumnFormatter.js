import React from "react";
import {
  OrganizationStatusCssClasses,
  OrganizationUserTitles,
} from "../../OrganizationUIHelpers";

export const AdminColumnFormatter = (cellContent, row) => {
  let index = cellContent ? 1 : 0;
  return (
    <span
      className={`label label-lg label-light-${OrganizationStatusCssClasses[index]} label-inline`}
    >
      {OrganizationUserTitles[index]}
    </span>
  );
};
