import { all } from "redux-saga/effects";
import { combineReducers } from "redux";

import * as auth from "../app/modules/Auth/_redux/authRedux";
import { appSlice } from "./app/appSlice";
import { newsSlice } from "../app/modules/NewsInfo/_redux/news/newsSlice";
import { organizationSlice } from "../app/modules/OrganizationInfo/_redux/organization/organizationSlice";
import { documentSlice } from "../app/modules/DocumentInfo/_redux/document/documentSlice";
import { sourceSlice } from "../app/modules/NewsInfo/_redux/source/sourceSlice";
import { newsImpactAssessmentSlice } from "../app/modules/NewsInfo/_redux/impact-assessment/impactAssessmentSlice";
import { industrySlice } from "../app/modules/ProductInfo/_redux/industry/industrySlice";
import { productCategorySlice } from "../app/modules/ProductInfo/_redux/product-category/productCategorySlice";
import { materialCategorySlice } from "../app/modules/ProductInfo/_redux/material-category/materialCategorySlice";
import { issuingbodySlice } from "../app/modules/RegulationInfo/_redux/issuingbody/issuingbodySlice";
import { usersSlice } from "../app/modules/OrganizationInfo/_redux/users/usersSlice";
import { regulatoryFrameworkSlice } from "../app/modules/RegulationInfo/_redux/regulatory-framework/regulatoryFrameworkSlice";
import { regulationSlice } from "../app/modules/RegulationInfo/_redux/regulation/regulationSlice";
import { impactAssessmentSlice } from "../app/modules/RegulationInfo/_redux/impact-assessment/impactAssessmentSlice";
import { substancesSlice } from "./substances/substancesSlice";
import { substanceDataSlice } from "../app/modules/SubstanceInfo/_redux/substance-data/substanceDataSlice";
import { familySlice } from "../app/modules/SubstanceInfo/_redux/family/familySlice";
import { limitSlice } from "../app/modules/LimitInfo/_redux/limit/limitSlice";
import { exemptionSlice } from "../app/modules/LimitInfo/_redux/exemption/exemptionSlice";
import { filtersSlice } from "../app/modules/LimitInfo/_redux/filters/filtersSlice";
import { regionDataSlice } from "../app/modules/RegionInfo/_redux/region/regionSlice";

export const rootReducer = combineReducers({
  auth: auth.reducer,
  app: appSlice.reducer,
  news: newsSlice.reducer,
  organization: organizationSlice.reducer,
  document: documentSlice.reducer,
  source: sourceSlice.reducer,
  industry: industrySlice.reducer,
  productCategory: productCategorySlice.reducer,
  materialCategory: materialCategorySlice.reducer,
  issuingbody: issuingbodySlice.reducer,
  users: usersSlice.reducer,
  regulatoryFramework: regulatoryFrameworkSlice.reducer,
  regulation: regulationSlice.reducer,
  impactAssessment: impactAssessmentSlice.reducer,
  newsImpactAssessment: newsImpactAssessmentSlice.reducer,
  substances: substancesSlice.reducer,
  substanceData: substanceDataSlice.reducer,
  family: familySlice.reducer,
  limit: limitSlice.reducer,
  exemption: exemptionSlice.reducer,
  filters: filtersSlice.reducer,
  region: regionDataSlice.reducer,
});

export function* rootSaga() {
  yield all([auth.saga()]);
}
