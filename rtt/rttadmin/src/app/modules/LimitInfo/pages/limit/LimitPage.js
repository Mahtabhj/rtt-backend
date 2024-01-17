import React  from "react";
import { useSelector } from "react-redux";

import { limitIsLoading } from "../../_redux/limit/limitSelectors";

import { LoadingDialog } from "@metronic-partials/controls";

import { LimitCard } from "./components/LimitCard";

export const LimitPage = () => {
  const isLoading = useSelector(limitIsLoading);

  return (
    <>
      <LoadingDialog isLoading={isLoading} text="Loading ..." />

      <LimitCard />
    </>
  );
}
