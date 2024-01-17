import React from "react";
import {
  IssuingBodyStatusCssClasses,
  IssuingBodyStatusTitles,
} from "../../IssuingBodyUIHelpers";

export const StatusColumnFormatter = (cellContent, row) => {
  let index = cellContent ? 0 : 1;
  return (
    <span
      className={`label label-lg label-light-${IssuingBodyStatusCssClasses[index]} label-inline`}
    >
      {IssuingBodyStatusTitles[index]}
    </span>
  );
};
