import React, { useMemo } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { IndustryTable } from "./industry-table/IndustryTable";
import { useIndustryUIContext } from "./IndustryUIContext";

export function IndustryCard() {
  const industryUIContext = useIndustryUIContext();
  const industryUIProps = useMemo(() => {
    return {
      ids: industryUIContext.ids,
      queryParams: industryUIContext.queryParams,
      setQueryParams: industryUIContext.setQueryParams,
      newIndustryButtonClick: industryUIContext.newIndustryButtonClick,
      openDeleteIndustryDialog: industryUIContext.openDeleteIndustryDialog,
      openEditIndustryPage: industryUIContext.openEditIndustryPage,
      openUpdateIndustryStatusDialog:
        industryUIContext.openUpdateIndustryStatusDialog,
      openFetchIndustryDialog: industryUIContext.openFetchIndustryDialog,
    };
  }, [industryUIContext]);

  return (
    <Card>
      <CardHeader title="Industry List">
        <CardHeaderToolbar>
          <button
            type="button"
            className="btn btn-primary"
            onClick={industryUIProps.newIndustryButtonClick}
          >
            Create Industry{" "}
          </button>
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        {industryUIProps.ids.length > 0 && <>{/* <IndustryGrouping /> */}</>}
        <IndustryTable />
      </CardBody>
    </Card>
  );
}
