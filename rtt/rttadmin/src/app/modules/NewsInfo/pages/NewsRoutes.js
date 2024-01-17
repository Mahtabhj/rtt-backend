import React, { Suspense } from 'react';
import { Redirect, Switch } from 'react-router-dom';

import { LayoutSplashScreen, ContentRoute } from '@metronic/layout';

import { NEWS, NEWS_ASSESSMENT_WORKFLOW, SOURCE } from '@common';
import { permissionsRoutePath } from '@common/Permissions/routesPaths';

import { NewsPage } from './news/NewsPage';
import { NewsEdit } from './news/news-edit/NewsEdit';
import { NewsSelect } from './news/news-select/NewsSelect';
import { SourcePage } from './source/SourcePage';
import { SourceEdit } from './source/source-edit/SourceEdit';
import { SourceSelect } from './source/source-select/SourceSelect';
import { ImpactAssessmentPage, ImpactAssessmentSelect } from './impact-assessment/ImpactAssessment';

const MAIN_PATH = permissionsRoutePath[NEWS];
const NEWS_TAB = NEWS;
const IMPACT_ASSESSMENT_TAB = 'impactAssessment';
const SOURCES_TAB = 'sources';

const NewsRoutes = () => (
  <Suspense fallback={<LayoutSplashScreen />}>
    <Switch>
      <ContentRoute
        path={`${MAIN_PATH}/${NEWS_TAB}/new`}
        component={NewsEdit}
        permission={NEWS}
        to={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${NEWS_TAB}/:id/edit`}
        component={NewsEdit}
        permission={NEWS}
        to={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${NEWS_TAB}/:id/select`}
        component={NewsSelect}
        permission={NEWS}
        to={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${NEWS_TAB}`}
        component={NewsPage}
        permission={NEWS}
        to={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}`}
      />

      <ContentRoute
        path={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}/:id/select`}
        component={ImpactAssessmentSelect}
        permission={NEWS_ASSESSMENT_WORKFLOW}
        to={`${MAIN_PATH}/${SOURCES_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${IMPACT_ASSESSMENT_TAB}`}
        component={ImpactAssessmentPage}
        permission={NEWS_ASSESSMENT_WORKFLOW}
        to={`${MAIN_PATH}/${SOURCES_TAB}`}
      />

      <ContentRoute
        path={`${MAIN_PATH}/${SOURCES_TAB}/new`}
        component={SourceEdit}
        permission={SOURCE}
        to={`${MAIN_PATH}/${NEWS_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${SOURCES_TAB}/:id/edit`}
        component={SourceEdit}
        permission={SOURCE}
        to={`${MAIN_PATH}/${NEWS_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${SOURCES_TAB}/:id/select`}
        component={SourceSelect}
        permission={SOURCE}
        to={`${MAIN_PATH}/${NEWS_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${SOURCES_TAB}`}
        component={SourcePage}
        permission={SOURCE}
        to={`${MAIN_PATH}/${NEWS_TAB}`}
      />

      <Redirect
        from='*'
        to={`${MAIN_PATH}/${NEWS_TAB}`}
      />
    </Switch>
  </Suspense>
)

export default NewsRoutes;