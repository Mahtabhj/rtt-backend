import React, { Suspense } from 'react';
import { Redirect, Switch } from 'react-router-dom';

import { LayoutSplashScreen, ContentRoute } from '@metronic/layout';

import { ANSWER, FRAMEWORK_PERMISSION, ISSUING_BODY, REGULATION } from '@common';
import { permissionsRoutePath } from '@common/Permissions/routesPaths';

import { RegulatoryFrameworkPage } from './regulatory-framework/RegulatoryFrameworkPage';
import { RegulatoryFrameworkEdit } from './regulatory-framework/regulatory-framework-edit/RegulatoryFrameworkEdit';
import { RegulatoryFrameworkSelect } from './regulatory-framework/regulatory-framework-select/RegulatoryFrameworkSelect';
import { RegulationPage } from './regulations/RegulationPage';
import { RegulationEdit } from './regulations/regulation-edit/RegulationEdit';
import { IssuingBodyPage } from './issuingbody/IssuingBodyPage';
import { IssuingBodyEdit } from './issuingbody/issuingbody-edit/IssuingBodyEdit';
import { IssuingBodySelect } from './issuingbody/issuingbody-select/IssuingBodySelect';
import { ImpactAssessmentPage } from './impact-assessment/ImpactAssessmentPage';
import { ImpactAssessmentEdit } from './impact-assessment/impact-assessment-edit/ImpactAssessmentEdit';

const MAIN_PATH = permissionsRoutePath[REGULATION];
const REGULATORY_FRAMEWORK_TAB = 'regulatory-framework';
const REGULATION_TAB = REGULATION;
const ISSUING_BODY_TAB = ISSUING_BODY;
const IMPACT_ASSESSMENT_TAB = 'impactAssessment';

const RegulationRoutes = () => (
  <Suspense fallback={<LayoutSplashScreen />}>
    <Switch>
      <ContentRoute
        path={`${MAIN_PATH}/${REGULATORY_FRAMEWORK_TAB}/new`}
        component={RegulatoryFrameworkEdit}
        permission={FRAMEWORK_PERMISSION}
        to={`${MAIN_PATH}/${REGULATION_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${REGULATORY_FRAMEWORK_TAB}/:id/edit`}
        component={RegulatoryFrameworkEdit}
        permission={FRAMEWORK_PERMISSION}
        to={`${MAIN_PATH}/${REGULATION_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${REGULATORY_FRAMEWORK_TAB}/:id/select`}
        component={RegulatoryFrameworkSelect}
        permission={FRAMEWORK_PERMISSION}
        to={`${MAIN_PATH}/${REGULATION_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${REGULATORY_FRAMEWORK_TAB}`}
        component={RegulatoryFrameworkPage}
        permission={FRAMEWORK_PERMISSION}
        to={`${MAIN_PATH}/${REGULATION_TAB}`}
      />

      <ContentRoute
        path={`${MAIN_PATH}/${REGULATION_TAB}/new`}
        component={RegulationEdit}
        permission={REGULATION}
        to={`${MAIN_PATH}/${ISSUING_BODY_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${REGULATION_TAB}/:id/edit`}
        component={RegulationEdit}
        permission={REGULATION}
        to={`${MAIN_PATH}/${ISSUING_BODY_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${REGULATION_TAB}`}
        component={RegulationPage}
        permission={REGULATION}
        to={`${MAIN_PATH}/${ISSUING_BODY_TAB}`}
      />

      <ContentRoute
        path={`${MAIN_PATH}/${ISSUING_BODY_TAB}/new`}
        component={IssuingBodyEdit}
        permission={ISSUING_BODY}
        to={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${ISSUING_BODY_TAB}/:id/edit`}
        component={IssuingBodyEdit}
        permission={ISSUING_BODY}
        to={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${ISSUING_BODY_TAB}/:id/select`}
        component={IssuingBodySelect}
        permission={ISSUING_BODY}
        to={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${ISSUING_BODY_TAB}`}
        component={IssuingBodyPage}
        permission={ISSUING_BODY}
        to={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}`}
      />

      <ContentRoute
        path={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}/:id/edit`}
        component={ImpactAssessmentEdit}
        permission={ANSWER}
        to={`${MAIN_PATH}/${REGULATORY_FRAMEWORK_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}`}
        component={ImpactAssessmentPage}
        permission={ANSWER}
        to={`${MAIN_PATH}/${REGULATORY_FRAMEWORK_TAB}`}
      />

      <Redirect
        from='*'
        to={`${MAIN_PATH}/${REGULATORY_FRAMEWORK_TAB}`}
      />
    </Switch>
  </Suspense>
)
export default RegulationRoutes;