import React from "react";
import {
  IssuingBodyConditionCssClasses,
  IssuingBodyConditionTitles,
} from "../../IssuingBodyUIHelpers";

export const ConditionColumnFormatter = (cellContent, row) => (
  <>
    <span
      className={`badge badge-${
        IssuingBodyConditionCssClasses[row.condition]
      } badge-dot`}
    ></span>
    &nbsp;
    <span
      className={`font-bold font-${
        IssuingBodyConditionCssClasses[row.condition]
      }`}
    >
      {IssuingBodyConditionTitles[row.condition]}
    </span>
  </>
);
