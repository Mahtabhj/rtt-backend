import React, { Suspense } from 'react';
import { Redirect, Switch } from 'react-router-dom';
import { LayoutSplashScreen, ContentRoute } from '@metronic/layout';

import { INDUSTRY, MATERIAL_CATEGORY, PRODUCT, PRODUCT_CATEGORY } from '@common';
import { permissionsRoutePath } from '@common/Permissions/routesPaths';

import { IndustryPage } from './industry/IndustryPage';
import { IndustryEdit } from './industry/industry-edit/IndustryEdit';
import { ProductCategoryPage } from './product-category/ProductCategoryPage';
import { ProductCategoryEdit } from './product-category/product-category-edit/ProductCategoryEdit';
import { MaterialCategoryPage } from './material-category/MaterialCategoryPage';
import { MaterialCategoryEdit } from './material-category/material-category-edit/MaterialCategoryEdit';

const MAIN_PATH = permissionsRoutePath[PRODUCT];
const INDUSTRIES_TAB = 'industries';
const PRODUCT_CATEGORIES_TAB = 'product-categories';
const MATERIAL_CATEGORIES_TAB = 'material-categories';

const ProductRoutes = () => (
  <Suspense fallback={<LayoutSplashScreen />}>
    <Switch>
      <ContentRoute
        path={`${MAIN_PATH}/${INDUSTRIES_TAB}/new`}
        component={IndustryEdit}
        permission={INDUSTRY}
        to={`${MAIN_PATH}/${PRODUCT_CATEGORIES_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${INDUSTRIES_TAB}/:id/edit`}
        component={IndustryEdit}
        permission={INDUSTRY}
        to={`${MAIN_PATH}/${PRODUCT_CATEGORIES_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${INDUSTRIES_TAB}`}
        component={IndustryPage}
        permission={INDUSTRY}
        to={`${MAIN_PATH}/${PRODUCT_CATEGORIES_TAB}`}
      />

      <ContentRoute
        path={`${MAIN_PATH}/${PRODUCT_CATEGORIES_TAB}/new`}
        component={ProductCategoryEdit}
        permission={PRODUCT_CATEGORY}
        to={`${MAIN_PATH}/${MATERIAL_CATEGORIES_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${PRODUCT_CATEGORIES_TAB}/:id/edit`}
        component={ProductCategoryEdit}
        permission={PRODUCT_CATEGORY}
        to={`${MAIN_PATH}/${MATERIAL_CATEGORIES_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${PRODUCT_CATEGORIES_TAB}`}
        component={ProductCategoryPage}
        permission={PRODUCT_CATEGORY}
        to={`${MAIN_PATH}/${MATERIAL_CATEGORIES_TAB}`}
      />

      <ContentRoute
        path={`${MAIN_PATH}/${MATERIAL_CATEGORIES_TAB}/new`}
        component={MaterialCategoryEdit}
        permission={MATERIAL_CATEGORY}
        to={`${MAIN_PATH}/${INDUSTRIES_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${MATERIAL_CATEGORIES_TAB}/:id/edit`}
        component={MaterialCategoryEdit}
        permission={MATERIAL_CATEGORY}
        to={`${MAIN_PATH}/${INDUSTRIES_TAB}`}
      />
      <ContentRoute
        path={`${MAIN_PATH}/${MATERIAL_CATEGORIES_TAB}`}
        component={MaterialCategoryPage}
        permission={MATERIAL_CATEGORY}
        to={`${MAIN_PATH}/${INDUSTRIES_TAB}`}
      />

      <Redirect
        from='*'
        to={`${MAIN_PATH}/${INDUSTRIES_TAB}`}
      />
    </Switch>
  </Suspense>
)

export default ProductRoutes;
