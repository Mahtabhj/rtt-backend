import React from "react";
import { useSelector } from "react-redux";
import { LoadingDialog } from "@metronic-partials/controls";

export function ImpactAssessmentLoadingDialog() {
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.newsImpactAssessment.listLoading })
  );
  return <LoadingDialog isLoading={isLoading} text="Loading ..." />;
}
