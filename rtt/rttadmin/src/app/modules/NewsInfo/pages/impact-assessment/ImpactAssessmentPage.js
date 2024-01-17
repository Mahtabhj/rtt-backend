import React from "react";
import { ImpactAssessmentLoadingDialog } from "./impact-assessment-loading-dialog/ImpactAssessmentLoadingDialog";
import { ImpactAssessmentCard } from "./ImpactAssessmentCard";
import { ImpactAssessmentUIProvider } from "./ImpactAssessmentUIContext";

export function ImpactAssessmentPage({ history }) {
  const impactAssessmentUIEvents = {
    openSelectImpactAssessmentPage: (id) => {
      history.push(`/backend/news-info/impactAssessment/${id}/select`);
    },
  };

  return (
    <ImpactAssessmentUIProvider impactAssessmentUIEvents={impactAssessmentUIEvents}>
      <ImpactAssessmentLoadingDialog />

      <ImpactAssessmentCard />
    </ImpactAssessmentUIProvider>
  );
}
