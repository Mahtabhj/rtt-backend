import React from "react";
import { UserStatusCssClasses, UserTitles } from "../../UsersUIHelpers";

export function AdminColumnFormatter(cellContent, row) {
  let index = cellContent ? 1 : 0;
  const getLabelCssClasses = () => {
    return `label label-lg label-light-${UserStatusCssClasses[index]} label-inline`;
  };
  return <span className={getLabelCssClasses()}>{UserTitles[index]}</span>;
}
