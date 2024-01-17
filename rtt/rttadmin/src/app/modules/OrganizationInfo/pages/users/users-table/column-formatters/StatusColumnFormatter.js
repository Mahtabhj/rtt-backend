import React from "react";
import {
  UserStatusCssClasses,
  OrganizationStatusTitles,
} from "../../UsersUIHelpers";

export function StatusColumnFormatter(cellContent, row) {
  let index = cellContent ? 0 : 1;
  const getLabelCssClasses = () => {
    return `label label-lg label-light-${UserStatusCssClasses[index]} label-inline`;
  };
  return (
    <span className={getLabelCssClasses()}>
      {OrganizationStatusTitles[index]}
    </span>
  );
}
