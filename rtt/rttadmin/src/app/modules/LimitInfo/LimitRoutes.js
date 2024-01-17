import React from 'react';
import { Redirect, Switch } from 'react-router-dom';

import { EXEMPTION, LIMIT, LIMIT_PERMISSION } from '@common';
import { permissionsRoutePath } from '@common/Permissions/routesPaths';
import { PermissionsRoute } from '@common/Permissions/PermissionsRoute';

import { LimitPage } from './pages/limit/LimitPage';
import { ExemptionPage } from './pages/exemption/ExemptionPage';

const MAIN_PATH = permissionsRoutePath[LIMIT];
const LIMIT_TAB = 'limit';
const EXEMPTION_TAB = 'exemption';

export const LimitRoutes = () => (
  <Switch>
    <PermissionsRoute
      exact
      path={`${MAIN_PATH}/${LIMIT_TAB}`}
      component={LimitPage}
      permissions={[LIMIT_PERMISSION]}
      to={`${MAIN_PATH}/${EXEMPTION_TAB}`}
    />

    <PermissionsRoute
      exact
      path={`${MAIN_PATH}/${EXEMPTION_TAB}`}
      component={ExemptionPage}
      permissions={[EXEMPTION]}
      to={`${MAIN_PATH}/${LIMIT_TAB}`}
    />

    <Redirect
      from='*'
      to={`${MAIN_PATH}/${LIMIT_TAB}`}
    />
  </Switch>
)
