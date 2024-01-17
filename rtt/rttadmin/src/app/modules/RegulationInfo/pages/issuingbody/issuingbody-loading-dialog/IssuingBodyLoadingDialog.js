import React, { useEffect } from "react";
import { shallowEqual, useSelector } from "react-redux";
import { LoadingDialog } from "@metronic-partials/controls";

export function IssuingBodyLoadingDialog() {
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.issuingbody.listLoading }),
    shallowEqual
  );
  useEffect(() => {}, [isLoading]);
  return <LoadingDialog isLoading={isLoading} text="Loading ..." />;
}
