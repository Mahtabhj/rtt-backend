import React from "react";
import {
  RegulatoryFrameworkConditionCssClasses,
  RegulatoryFrameworkConditionTitles,
} from "../../RegulatoryFrameworkUIHelpers";

export const ConditionColumnFormatter = (cellContent, row) => (
  <>
    <span
      className={`badge badge-${
        RegulatoryFrameworkConditionCssClasses[row.condition]
      } badge-dot`}
    ></span>
    &nbsp;
    <span
      className={`font-bold font-${
        RegulatoryFrameworkConditionCssClasses[row.condition]
      }`}
    >
      {RegulatoryFrameworkConditionTitles[row.condition]}
    </span>
  </>
);
