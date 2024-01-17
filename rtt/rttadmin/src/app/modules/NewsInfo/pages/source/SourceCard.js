import React, { useMemo } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { SourceTable } from "./source-table/SourceTable";
import { SourceGrouping } from "./source-grouping/SourceGrouping";
import { useSourceUIContext } from "./SourceUIContext";

export function SourceCard() {
  const sourceUIContext = useSourceUIContext();
  const sourceUIProps = useMemo(() => {
    return {
      ids: sourceUIContext.ids,
      queryParams: sourceUIContext.queryParams,
      setQueryParams: sourceUIContext.setQueryParams,
      newSourceButtonClick: sourceUIContext.newSourceButtonClick,
      openDeleteSourcesDialog: sourceUIContext.openDeleteSourcesDialog,
      openEditSourcePage: sourceUIContext.openEditSourcePage,
      openSelectSourcePage: sourceUIContext.openSelectSourcePage,
      openUpdateSourceStatusDialog:
        sourceUIContext.openUpdateSourceStatusDialog,
      openFetchSourceDialog: sourceUIContext.openFetchSourceDialog,
    };
  }, [sourceUIContext]);

  return (
    <Card>
      <CardHeader title="Source List">
        <CardHeaderToolbar>
          <button
            type="button"
            className="btn btn-primary"
            onClick={sourceUIProps.newSourceButtonClick}
          >
            Create Source
          </button>
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        {sourceUIProps.ids.length > 0 && (
          <SourceGrouping />
        )}
        <SourceTable />
      </CardBody>
    </Card>
  );
}
