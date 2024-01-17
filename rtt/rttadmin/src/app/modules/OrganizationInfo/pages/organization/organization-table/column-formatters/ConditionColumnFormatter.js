import React from "react";
import {
  OrganizationConditionCssClasses,
  OrganizationConditionTitles
} from "../../OrganizationUIHelpers";

export const ConditionColumnFormatter = (cellContent, row) => (
  <>
    <span
      className={`badge badge-${
        OrganizationConditionCssClasses[row.condition]
      } badge-dot`}
    ></span>
    &nbsp;
    <span
      className={`font-bold font-${
        OrganizationConditionCssClasses[row.condition]
      }`}
    >
      {OrganizationConditionTitles[row.condition]}
    </span>
  </>
);
