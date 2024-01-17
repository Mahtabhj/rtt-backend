import React from "react";
import { useSelector } from "react-redux";

import { familyIsLoading } from "../../_redux/family/familySelectors";

import { LoadingDialog } from "@metronic-partials/controls";

import { FamilyCard } from "./components/FamilyCard";

export const FamilyPage = () => {
  const isLoading = useSelector(familyIsLoading);

  return (
    <>
      <LoadingDialog isLoading={isLoading} text="Loading ..." />

      <FamilyCard />
    </>
  );
}
