import React from "react";
import {
  SourceConditionCssClasses,
  SourceConditionTitles,
} from "../../SourceUIHelpers";

export const ConditionColumnFormatter = (cellContent, row) => (
  <>
    <span
      className={`badge badge-${
        SourceConditionCssClasses[row.condition]
      } badge-dot`}
    ></span>
    &nbsp;
    <span
      className={`font-bold font-${SourceConditionCssClasses[row.condition]}`}
    >
      {SourceConditionTitles[row.condition]}
    </span>
  </>
);
