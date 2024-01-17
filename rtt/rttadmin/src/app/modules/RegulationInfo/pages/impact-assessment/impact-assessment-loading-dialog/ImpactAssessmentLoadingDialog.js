import React, { useEffect } from "react";
import { shallowEqual, useSelector } from "react-redux";
import { LoadingDialog } from "@metronic-partials/controls";

export function ImpactAssessmentLoadingDialog() {
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.impactAssessment.listLoading }),
    shallowEqual
  );
  useEffect(() => {}, [isLoading]);
  return <LoadingDialog isLoading={isLoading} text="Loading ..." />;
}
