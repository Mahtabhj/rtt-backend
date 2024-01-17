import { PermissionsWrapper } from "./PermissionsWrapper";
import { DOCUMENT, LIMIT, REGULATION } from "../constants";

export const AuthorizeRegulation = props => PermissionsWrapper({ ...props, permissions: [REGULATION]});
export const AuthorizeLimit = props => PermissionsWrapper({ ...props, permissions: [LIMIT]});
export const AuthorizeDocument = props => PermissionsWrapper({ ...props, permissions: [DOCUMENT]});