import React from 'react';
import { Redirect, Switch } from 'react-router-dom';

import { REGION } from '@common';
import { permissionsRoutePath } from '@common/Permissions/routesPaths';
import { PermissionsRoute } from '@common/Permissions/PermissionsRoute';

import { RegionPage } from './region/RegionPage';

const MAIN_PATH = permissionsRoutePath[REGION];
const REGION_TAB = 'region';

export const RegionRoutes = () => (
	<Switch>
		<PermissionsRoute
			exact
			path={`${MAIN_PATH}/${REGION_TAB}`}
			component={RegionPage}
			permissions={[REGION]}
			to={`${MAIN_PATH}/${REGION_TAB}`}
		/>

		<Redirect
			from='*'
			to={`${MAIN_PATH}/${REGION_TAB}`}
		/>
	</Switch>
);