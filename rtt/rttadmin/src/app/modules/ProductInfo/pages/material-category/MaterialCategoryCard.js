import React, { useMemo } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { MaterialCategoryTable } from "./material-category-table/MaterialCategoryTable";
import { useMaterialCategoryUIContext } from "./MaterialCategoryUIContext";

export function MaterialCategoryCard() {
  const materialCategoryUIContext = useMaterialCategoryUIContext();
  const materialCategoryUIProps = useMemo(() => {
    return {
      ids: materialCategoryUIContext.ids,
      queryParams: materialCategoryUIContext.queryParams,
      setQueryParams: materialCategoryUIContext.setQueryParams,
      newMaterialCategoryButtonClick: materialCategoryUIContext.newMaterialCategoryButtonClick,
      openDeleteMaterialCategoryDialog: materialCategoryUIContext.openDeleteMaterialCategoryDialog,
      openEditMaterialCategoryPage:materialCategoryUIContext.openEditMaterialCategoryPage,
      openUpdateMaterialCategoryStatusDialog: materialCategoryUIContext.openUpdateMaterialCategoryStatusDialog,
      openFetchMaterialCategoryDialog: materialCategoryUIContext.openFetchMaterialCategoryDialog,
    };
  }, [materialCategoryUIContext]);

  return (
    <Card>
      <CardHeader title="Material Category List">
        <CardHeaderToolbar>
          <button
            type="button"
            className="btn btn-primary"
            onClick={materialCategoryUIProps.newMaterialCategoryButtonClick}
          >
            Create Material Category{" "}
          </button>
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        {materialCategoryUIProps.ids.length > 0}
        <MaterialCategoryTable />
      </CardBody>
    </Card>
  );
}
