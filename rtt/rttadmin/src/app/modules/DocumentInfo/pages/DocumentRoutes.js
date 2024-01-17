import React, { Suspense } from 'react';
import { Redirect, Switch } from 'react-router-dom';

import { LayoutSplashScreen, ContentRoute } from '@metronic/layout';

import { DOCUMENT } from '@common';
import { permissionsRoutePath } from '@common/Permissions/routesPaths';

import { DocumentPage } from './document/DocumentPage';
import { DocumentEdit } from './document/document-edit/DocumentEdit';
import { DocumentSelect } from './document/document-select/DocumentSelect';

const MAIN_PATH = permissionsRoutePath[DOCUMENT];
const DOCUMENTS_TAB = 'documents';

const DocumentRoutes = () => (
  <Suspense fallback={<LayoutSplashScreen />}>
    <Switch>
      <ContentRoute
        path={`${MAIN_PATH}/${DOCUMENTS_TAB}/new`}
        component={DocumentEdit}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${DOCUMENTS_TAB}/:id/edit`}
        component={DocumentEdit}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${DOCUMENTS_TAB}/:id/select`}
        component={DocumentSelect}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${DOCUMENTS_TAB}`}
        component={DocumentPage}
      />

      <Redirect
        from='*'
        to={`${MAIN_PATH}/${DOCUMENTS_TAB}`}
      />
    </Switch>
  </Suspense>
)

export default DocumentRoutes;
