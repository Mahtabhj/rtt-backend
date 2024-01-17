import { NEWS, REGULATION, REGULATORY_FRAMEWORK } from "../constants";

const visibleToOrganizationsContent = {
  title: {
    [NEWS]: 'News',
    [REGULATION]: 'Regulation',
    [REGULATORY_FRAMEWORK]: 'Regulatory Framework'
  }
};

export { visibleToOrganizationsContent as default };