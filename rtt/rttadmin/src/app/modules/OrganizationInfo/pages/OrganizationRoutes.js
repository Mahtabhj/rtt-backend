import React, { Suspense } from 'react';
import { Redirect, Switch } from 'react-router-dom';

import { LayoutSplashScreen, ContentRoute } from '@metronic/layout';

import { ORGANIZATION, USER } from '@common';
import { permissionsRoutePath } from '@common/Permissions/routesPaths';

import { OrganizationPage } from './organization/OrganizationPage';
import { OrganizationEdit } from './organization/organization-edit/OrganizationEdit';
import { UsersPage } from './users/UsersPage';

const MAIN_PATH = permissionsRoutePath[ORGANIZATION];
const ORGANIZATIONS_TAB = 'organizations';
const USERS_TAB = 'users';

const OrganizationRoutes = () => (
  <Suspense fallback={<LayoutSplashScreen/>}>
    <Switch>
      <ContentRoute
        path={`${MAIN_PATH}/${ORGANIZATIONS_TAB}/new`}
        component={OrganizationEdit}
        permission={ORGANIZATION}
        to={`${MAIN_PATH}/${USERS_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${ORGANIZATIONS_TAB}/:id/edit`}
        component={OrganizationEdit}
        permission={ORGANIZATION}
        to={`${MAIN_PATH}/${USERS_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${ORGANIZATIONS_TAB}`}
        component={OrganizationPage}
        permission={ORGANIZATION}
        to={`${MAIN_PATH}/${USERS_TAB}`}
      />

      <ContentRoute
        path={`${MAIN_PATH}/${USERS_TAB}`}
        component={UsersPage}
        permission={USER}
        to={`${MAIN_PATH}/${ORGANIZATIONS_TAB}`}
      />

      <Redirect
        from='*'
        to={`${MAIN_PATH}/${ORGANIZATIONS_TAB}`}
      />
    </Switch>
  </Suspense>
)

export default OrganizationRoutes;
