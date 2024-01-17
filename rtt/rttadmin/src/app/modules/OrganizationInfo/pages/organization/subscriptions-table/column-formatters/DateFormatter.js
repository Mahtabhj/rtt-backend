import React from "react";
import dayjs from "dayjs";

export const DateFormatter = (cellContent, row) => {
  return <span>{dayjs(cellContent).format("YYYY-MM-DD")}</span>;
};
