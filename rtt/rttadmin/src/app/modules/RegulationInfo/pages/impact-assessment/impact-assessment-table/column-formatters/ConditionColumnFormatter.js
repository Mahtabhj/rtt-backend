import React from "react";
import {
  ImpactAssessmentConditionCssClasses,
  ImpactAssessmentConditionTitles,
} from "../../ImpactAssessmentUIHelpers";

export const ConditionColumnFormatter = (cellContent, row) => (
  <>
    <span
      className={`badge badge-${
        ImpactAssessmentConditionCssClasses[row.condition]
      } badge-dot`}
    ></span>
    &nbsp;
    <span
      className={`font-bold font-${
        ImpactAssessmentConditionCssClasses[row.condition]
      }`}
    >
      {ImpactAssessmentConditionTitles[row.condition]}
    </span>
  </>
);
