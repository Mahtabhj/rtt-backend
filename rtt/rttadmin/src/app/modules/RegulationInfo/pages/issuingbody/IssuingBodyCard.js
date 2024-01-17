import React, { useMemo } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { IssuingBodyTable } from "./issuingbody-table/IssuingBodyTable";
import { useIssuingBodyUIContext } from "./IssuingBodyUIContext";

export function IssuingBodyCard() {
  const issuingbodyUIContext = useIssuingBodyUIContext();
  const issuingbodyUIProps = useMemo(() => {
    return {
      ids: issuingbodyUIContext.ids,
      queryParams: issuingbodyUIContext.queryParams,
      setQueryParams: issuingbodyUIContext.setQueryParams,
      newIssuingBodyButtonClick: issuingbodyUIContext.newIssuingBodyButtonClick,
      openDeleteIssuingBodysDialog:
        issuingbodyUIContext.openDeleteIssuingBodysDialog,
      openEditIssuingBodyPage: issuingbodyUIContext.openEditIssuingBodyPage,
      openSelectIssuingBodyPage: issuingbodyUIContext.openSelectIssuingBodyPage,
      openUpdateIssuingBodyStatusDialog:
        issuingbodyUIContext.openUpdateIssuingBodyStatusDialog,
      openFetchIssuingBodyDialog:
        issuingbodyUIContext.openFetchIssuingBodyDialog,
    };
  }, [issuingbodyUIContext]);

  return (
    <Card>
      <CardHeader title="Issuing Body List">
        <CardHeaderToolbar>
          <button
            type="button"
            className="btn btn-primary"
            onClick={issuingbodyUIProps.newIssuingBodyButtonClick}
          >
            Create Issuing Body
          </button>
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        <IssuingBodyTable />
      </CardBody>
    </Card>
  );
}
