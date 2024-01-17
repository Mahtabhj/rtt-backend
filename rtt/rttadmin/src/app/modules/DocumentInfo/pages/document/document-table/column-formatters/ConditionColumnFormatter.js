import React from "react";
import {
  DocumentConditionCssClasses,
  DocumentConditionTitles,
} from "../../DocumentUIHelpers";

export const ConditionColumnFormatter = (cellContent, row) => (
  <>
    <span
      className={`badge badge-${
        DocumentConditionCssClasses[row.condition]
      } badge-dot`}
    ></span>
    &nbsp;
    <span
      className={`font-bold font-${DocumentConditionCssClasses[row.condition]}`}
    >
      {DocumentConditionTitles[row.condition]}
    </span>
  </>
);
