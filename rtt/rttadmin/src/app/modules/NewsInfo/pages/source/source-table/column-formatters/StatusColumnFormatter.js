import React from "react";
import {
  SourceStatusCssClasses,
  SourceStatusTitles,
} from "../../SourceUIHelpers";

export const StatusColumnFormatter = (cellContent, row) => {
  let index = cellContent ? 0 : 1;
  return (
    <span
      className={`label label-lg label-light-${SourceStatusCssClasses[index]} label-inline`}
    >
      {SourceStatusTitles[index]}
    </span>
  );
};
