import React from "react";
import {
  RegulationStatusCssClasses,
  RegulationStatusTitles,
} from "../../RegulationUIHelpers";

export const StatusColumnFormatter = (cellContent, row) => {
  let index = cellContent == false ? 0 : 1;
  return (
    <span
      className={`label label-lg label-light-${RegulationStatusCssClasses[index]} label-inline`}
    >
      {RegulationStatusTitles[index]}
    </span>
  );
};
