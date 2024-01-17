import React from "react";
import { ImpactAssessmentLoadingDialog } from "./impact-assessment-loading-dialog/ImpactAssessmentLoadingDialog";
import { ImpactAssessmentCard } from "./ImpactAssessmentCard";
import { ImpactAssessmentUIProvider } from "./ImpactAssessmentUIContext";

export function ImpactAssessmentPage({ history }) {
  const impactAssessmentUIEvents = {
    openEditImpactAssessmentPage: (id) => {
      history.push(`/backend/regulation-info/impactAssessment/${id}/edit`);
    },
    openFetchImpactAssessmentDialog: () => {
      history.push(`/backend/regulation-info/impactAssessment/fetch`);
    },
    openUpdateImpactAssessmentStatusDialog: () => {
      history.push("/backend/regulation-info/impactAssessment/updateStatus");
    },
  };

  return (
    <ImpactAssessmentUIProvider impactAssessmentUIEvents={impactAssessmentUIEvents}>
      <ImpactAssessmentLoadingDialog />

      <ImpactAssessmentCard />
    </ImpactAssessmentUIProvider>
  );
}
