export const DEBOUNCE_TIMEOUT = 400;
export const TOOLTIP_DELAY = 300;
export const ENTER_KEYCODE = 13;

export const TITLE_LIMIT_SHORT = 50;
export const TITLE_LIMIT_ULTRASHORT = 30;

export const DATE_FORMAT = 'DD/MM/YY';
export const DATE_FULL_YEAR_FORMAT = 'DD/MM/YYYY';
export const DATE_FORMAT_FOR_REQUEST = 'YYYY-MM-DD';

export const DASHBOARD = 'dashboard';
export const ORGANIZATION = 'organization';
export const USER = 'user';
export const NEWS = 'news';
export const NEWS_ASSESSMENT_WORKFLOW = 'newsassessmentworkflow';
export const SOURCE = 'source';
export const REGULATORY_FRAMEWORK = 'regulatoryFramework';
export const REGION = 'region';
export const FRAMEWORK_PERMISSION = REGULATORY_FRAMEWORK.toLowerCase();
export const REGULATION = 'regulation';
export const ISSUING_BODY = 'issuingbody';
export const ANSWER = 'answer';
export const SUBSTANCE = 'substance';
export const SUBSTANCE_FAMILY = 'substancefamily';
export const LIMIT = 'limit';
export const LIMIT_PERMISSION = 'regulationsubstancelimit';
export const EXEMPTION = 'exemption';
export const INDUSTRY = 'industry';
export const PRODUCT_CATEGORY = 'productcategory';
export const MATERIAL_CATEGORY = 'materialcategory';
export const PRODUCT = 'product';
export const DOCUMENT = 'document';

export const TAB_RELATED_REGULATIONS = 'Related Regulations';
export const TAB_USEFUL_LINKS = 'Useful Links';
export const TAB_DOCUMENTS = 'Documents';
export const TAB_MILESTONES = 'Milestones';
export const TAB_IMPACT_ASSESSMENT = 'Impact Assessment';
export const TAB_RELATED_SUBSTANCES = 'Related Substances';

export const MANUAL_ADD = 'Manual add';
export const UPLOAD_FILE = 'Upload file';

export const REVIEW = 'review';

export const BUTTON = {
  SAVE: 'save',
  CANCEL: 'cancel',
};

export const ACTION_TYPE = {
  PENDING: 'pending',
  FULFILLED: 'fulfilled',
  REJECTED: 'rejected',
};

export const reviewStatus = {
  'o': 'Online',
  'd': 'Draft',
};

export const statusOptions = [
  { value: 'active', title: 'Active' },
  { value: 'deleted', title: 'Deleted' }
];

export const initialValuesForRelevantOrganization = {
  product_categories: [],
  material_categories: [],
  topics: [],
  regulations: [],
  frameworks: [],
};
