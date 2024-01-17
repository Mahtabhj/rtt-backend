import React  from "react";
import { useSelector } from "react-redux";

import { exemptionIsLoading } from "../../_redux/exemption/exemptionSelectors";

import { LoadingDialog } from "@metronic-partials/controls";

import { ExemptionCard } from "./components/ExemptionCard";

export const ExemptionPage = () => {
  const isLoading = useSelector(exemptionIsLoading);

  return (
    <>
      <LoadingDialog isLoading={isLoading} text="Loading ..." />

      <ExemptionCard />
    </>
  );
}
