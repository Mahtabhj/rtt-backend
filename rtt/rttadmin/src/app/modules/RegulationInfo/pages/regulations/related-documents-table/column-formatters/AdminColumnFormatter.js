import React from "react";
import {
  RegulationStatusCssClasses,
  RegulationStatusTitles,
} from "../../RegulationUIHelpers";

export const AdminColumnFormatter = (cellContent, row) => {
  let index = cellContent === "True" ? 0 : 1;
  return (
    <span
      className={`label label-lg label-light-${RegulationStatusCssClasses[index]} label-inline`}
    >
      {RegulationStatusTitles[index]}
    </span>
  );
};
