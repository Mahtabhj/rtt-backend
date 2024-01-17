import React from "react";
import {
  ImpactAssessmentStatusCssClasses,
  ImpactAssessmentStatusTitles,
} from "../../ImpactAssessmentUIHelpers";

export const StatusColumnFormatter = (cellContent, row) => {
  let index = cellContent ? 0 : 1;
  return (
    <span
      className={`label label-lg label-light-${ImpactAssessmentStatusCssClasses[index]} label-inline`}
    >
      {ImpactAssessmentStatusTitles[index]}
    </span>
  );
};
