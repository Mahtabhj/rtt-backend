import React from "react";
import PropTypes from "prop-types";
import { useSelector } from "react-redux";

import { getSuperuserKeyFromJwt } from "../index";

const propTypes = {
  children: PropTypes.element.isRequired,
  permissions: PropTypes.arrayOf(PropTypes.string.isRequired).isRequired,
};

export const PermissionsWrapper = ({ children, permissions }) => {
  const { isSuperuser, permissionsList = [] } = useSelector(
    (state) => ({
      isSuperuser: getSuperuserKeyFromJwt(state.auth.authToken),
      permissionsList: state.auth.permissions,
    })
  );

  const isAllowedPermission = !permissions.length || permissions.some(permission => permissionsList.includes(permission));

  return (isSuperuser || isAllowedPermission) ? children : <></>;
};

PermissionsWrapper.propTypes = propTypes;
