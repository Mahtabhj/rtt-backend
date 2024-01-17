import React from "react";
import {
  RegulatoryFrameworkStatusCssClasses,
  RegulatoryFrameworkStatusTitles,
} from "../../RegulatoryFrameworkUIHelpers";

export const AdminColumnFormatter = (cellContent, row) => {
  let index = cellContent === "True" ? 0 : 1;
  return (
    <span
      className={`label label-lg label-light-${RegulatoryFrameworkStatusCssClasses[index]} label-inline`}
    >
      {RegulatoryFrameworkStatusTitles[index]}
    </span>
  );
};
