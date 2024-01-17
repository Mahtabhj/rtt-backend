import React from "react";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { ImpactAssessmentTable } from "./impact-assessment-table/ImpactAssessmentTable";

export function ImpactAssessmentCard() {
  return (
    <Card>
      <CardHeader title="Impact Assessment List">
        <CardHeaderToolbar />
      </CardHeader>

      <CardBody>
        <ImpactAssessmentTable />
      </CardBody>
    </Card>
  );
}
