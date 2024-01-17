import { DOCUMENT, LIMIT, NEWS, ORGANIZATION, PRODUCT, REGULATION, SUBSTANCE, REGION } from "../index";

export const  permissionsRoutePath = {
  [ORGANIZATION]: '/backend/organization-info',
  [NEWS]: '/backend/news-info',
  [REGULATION]: '/backend/regulation-info',
  [SUBSTANCE]: '/backend/substance-info',
  [LIMIT]: '/backend/limit-info',
  [PRODUCT]: '/backend/product-info',
  [DOCUMENT]: '/backend/document-info',
  [REGION]: '/backend/region-info',
};

export const dashboardRoutePath = '/backend/dashboard';