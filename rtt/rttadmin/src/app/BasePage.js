import React, { Suspense, lazy, useEffect } from "react";
import { Redirect, Switch, useHistory } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";

import { actions } from "@redux-auth/authRedux";

import { LayoutSplashScreen, ContentRoute } from "@metronic/layout";

import { PermissionsRoute } from "./common/Permissions/PermissionsRoute";

import { DashboardPage } from "./pages/DashboardPage";
import { SubstanceRoutes } from "./modules/SubstanceInfo/SubstanceRoutes";
import { RegionRoutes } from "./modules/RegionInfo/pages/RegionRoutes";
import { LimitRoutes } from "./modules/LimitInfo/LimitRoutes";

import { dashboardRoutePath, permissionsRoutePath } from "./common/Permissions/routesPaths";
import {
  ANSWER,
  DOCUMENT,
  EXEMPTION,
  FRAMEWORK_PERMISSION,
  INDUSTRY,
  ISSUING_BODY,
  LIMIT,
  LIMIT_PERMISSION,
  MATERIAL_CATEGORY,
  NEWS,
  NEWS_ASSESSMENT_WORKFLOW,
  ORGANIZATION,
  PRODUCT,
  PRODUCT_CATEGORY,
  REGULATION,
  SOURCE, SUBSTANCE,
  SUBSTANCE_FAMILY,
  USER,
  REGION
} from "./common";

const OrganizationRoutes = lazy(() => import("./modules/OrganizationInfo/pages/OrganizationRoutes"));
const NewsRoutes = lazy(() => import("./modules/NewsInfo/pages/NewsRoutes"));
const RegulationRoutes = lazy(() => import("./modules/RegulationInfo/pages/RegulationRoutes"));
const ProductRoutes = lazy(() => import("./modules/ProductInfo/pages/ProductRoutes"));
const DocumentRoutes = lazy(() => import("./modules/DocumentInfo/pages/DocumentRoutes"));

export default function BasePage() {
  const { location } = useHistory();
  const dispatch = useDispatch();

  const { isPermissionsLoaded } = useSelector(state => state.auth);

  useEffect(() => {
    dispatch(actions.requestUser());
  }, [dispatch, location]);

  useEffect(() => {
    dispatch(actions.requestPermissions());
  }, [dispatch]);

  return (
    <Suspense fallback={<LayoutSplashScreen />}>
      <Switch>
        <Redirect exact from="/" to={dashboardRoutePath} />
        <Redirect exact from="/backend/" to={dashboardRoutePath} />

        <ContentRoute path={dashboardRoutePath} component={DashboardPage} />

        {isPermissionsLoaded && (
          <>
            <PermissionsRoute
              path={permissionsRoutePath[ORGANIZATION]}
              component={OrganizationRoutes}
              permissions={[ORGANIZATION, USER]}
            />
            <PermissionsRoute
              path={permissionsRoutePath[NEWS]}
              component={NewsRoutes}
              permissions={[NEWS, NEWS_ASSESSMENT_WORKFLOW, SOURCE]}
            />
            <PermissionsRoute
              path={permissionsRoutePath[REGULATION]}
              component={RegulationRoutes}
              permissions={[FRAMEWORK_PERMISSION, REGULATION, ISSUING_BODY, ANSWER]}
            />
            <PermissionsRoute
              path={permissionsRoutePath[SUBSTANCE]}
              component={SubstanceRoutes}
              permissions={[SUBSTANCE, SUBSTANCE_FAMILY]}
            />
            <PermissionsRoute
              path={permissionsRoutePath[LIMIT]}
              component={LimitRoutes}
              permissions={[LIMIT_PERMISSION, EXEMPTION]}
            />
            <PermissionsRoute
              path={permissionsRoutePath[PRODUCT]}
              component={ProductRoutes}
              permissions={[INDUSTRY, PRODUCT_CATEGORY, MATERIAL_CATEGORY]}
            />
            <PermissionsRoute
              path={permissionsRoutePath[DOCUMENT]}
              component={DocumentRoutes}
              permissions={[DOCUMENT]}
            />
            <PermissionsRoute
              path={permissionsRoutePath[REGION]}
              component={RegionRoutes}
              permissions={[REGION]}
            />
          </>
        )}
      </Switch>
    </Suspense>
  );
}
