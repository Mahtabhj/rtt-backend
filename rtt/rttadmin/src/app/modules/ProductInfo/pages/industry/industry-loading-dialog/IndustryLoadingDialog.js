import React, { useEffect } from "react";
import { shallowEqual, useSelector } from "react-redux";
import { LoadingDialog } from "@metronic-partials/controls";

export function IndustryLoadingDialog() {
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.industry.listLoading }),
    shallowEqual
  );
  useEffect(() => {}, [isLoading]);
  return <LoadingDialog isLoading={isLoading} text="Loading ..." />;
}
