import React from "react";
import {
  UserTypeCssClasses,
  UserTypeTitles,
} from "../../UsersUIHelpers";

export function TypeColumnFormatter(cellContent, row) {
  return (
    <>
      <span
        className={`label label-dot label-${
          UserTypeCssClasses[row.type]
        } mr-2`}
      ></span>
      &nbsp;
      <span className={`font-bold font-${UserTypeCssClasses[row.type]}`}>
        {UserTypeTitles[row.type]}
      </span>
    </>
  );
}
