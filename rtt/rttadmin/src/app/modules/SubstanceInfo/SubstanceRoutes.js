import React from 'react';
import { Redirect, Switch } from 'react-router-dom';

import { SUBSTANCE, SUBSTANCE_FAMILY } from '@common';
import { permissionsRoutePath } from '@common/Permissions/routesPaths';
import { PermissionsRoute } from '@common/Permissions/PermissionsRoute';

import { SubstanceDataPage } from './pages/substance-data/SubstanceDataPage';
import { FamilyPage } from './pages/family/FamilyPage';
import { FamilyEditPage } from './pages/family/FamilyEditPage';

export const SUBSTANCE_MAIN_PATH = permissionsRoutePath[SUBSTANCE];
const SUBSTANCE_TAB = 'substance';
export const FAMILY_TAB = 'family';

export const SubstanceRoutes = () => (
  <Switch>
    <PermissionsRoute
      exact
      path={`${SUBSTANCE_MAIN_PATH}/${SUBSTANCE_TAB}`}
      component={SubstanceDataPage}
      permissions={[SUBSTANCE]}
      to={`${SUBSTANCE_MAIN_PATH}/${FAMILY_TAB}`}
    />

    <PermissionsRoute
      exact
      path={`${SUBSTANCE_MAIN_PATH}/${FAMILY_TAB}/:id/edit`}
      component={FamilyEditPage}
      permissions={[SUBSTANCE_FAMILY]}
      to={`${SUBSTANCE_MAIN_PATH}/${SUBSTANCE_TAB}`}
    />
    <PermissionsRoute
      exact
      path={`${SUBSTANCE_MAIN_PATH}/${FAMILY_TAB}`}
      component={FamilyPage}
      permissions={[SUBSTANCE_FAMILY]}
      to={`${SUBSTANCE_MAIN_PATH}/${SUBSTANCE_TAB}`}
    />

    <Redirect
      from='*'
      to={`${SUBSTANCE_MAIN_PATH}/${SUBSTANCE_TAB}`}
    />
  </Switch>
)
