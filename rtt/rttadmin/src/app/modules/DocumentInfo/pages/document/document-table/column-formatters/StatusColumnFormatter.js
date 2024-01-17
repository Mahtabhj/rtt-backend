import React from "react";
import {
  DocumentStatusCssClasses,
  DocumentStatusTitles,
} from "../../DocumentUIHelpers";

export const StatusColumnFormatter = (cellContent, row) => {
  let index = cellContent ? 0 : 1;
  return (
    <span
      className={`label label-lg label-light-${DocumentStatusCssClasses[index]} label-inline`}
    >
      {DocumentStatusTitles[index]}
    </span>
  );
};
