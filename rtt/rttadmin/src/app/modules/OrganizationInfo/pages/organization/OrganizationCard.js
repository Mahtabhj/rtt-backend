import React, {useMemo} from "react";
import { Card, CardBody, CardHeader, CardHeaderToolbar} from "@metronic-partials/controls";
import { OrganizationTable } from "./organization-table/OrganizationTable";
import { OrganizationGrouping } from "./organization-grouping/OrganizationGrouping";
import { useOrganizationUIContext } from "./OrganizationUIContext";

export function OrganizationCard() {
  const organizationUIContext = useOrganizationUIContext();
  const organizationUIProps = useMemo(() => {
    return {
      ids: organizationUIContext.ids,
      queryParams: organizationUIContext.queryParams,
      setQueryParams: organizationUIContext.setQueryParams,
      newOrganizationButtonClick: organizationUIContext.newOrganizationButtonClick,
      openDeleteOrganizationsDialog: organizationUIContext.openDeleteOrganizationsDialog,
      openEditOrganizationPage: organizationUIContext.openEditOrganizationPage,
      openSelectOrganizationPage: organizationUIContext.openSelectOrganizationPage,
      openUpdateOrganizationStatusDialog: organizationUIContext.openUpdateOrganizationStatusDialog,
      openFetchOrganizationDialog: organizationUIContext.openFetchOrganizationDialog,
    };
  }, [organizationUIContext]);

  return (
    <Card>

      <CardHeader title="Organization List">
        <CardHeaderToolbar>
          <button type="button" className="btn btn-primary" onClick={organizationUIProps.newOrganizationButtonClick}>Create Organization </button>
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        {organizationUIProps.ids.length > 0 && (
          <>
            <OrganizationGrouping />
          </>
        )}
        <OrganizationTable />
      </CardBody>

    </Card>
  );
}
