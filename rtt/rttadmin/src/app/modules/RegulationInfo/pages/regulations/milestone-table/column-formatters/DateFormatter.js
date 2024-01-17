import React from "react";
import dayjs from "dayjs";

export const DateFormatter = (cellContent, row) => {
  return <span>{cellContent ? dayjs(cellContent).format("DD/MM/YYYY") : ''}</span>;
};
