import React from "react";
import { Redirect, Route } from "react-router-dom";
import PropTypes from "prop-types";
import { useSelector } from "react-redux";

import { getSuperuserKeyFromJwt } from "../index";

const propTypes = {
  path: PropTypes.string.isRequired,
  component: PropTypes.oneOfType([PropTypes.object, PropTypes.string, PropTypes.func]).isRequired,
  permissions: PropTypes.arrayOf(PropTypes.string.isRequired).isRequired,
  to: PropTypes.string,
  exact: PropTypes.bool,
};

const defaultProps = {
  to: '/backend/dashboard',
  exact: false,
};

export const PermissionsRoute = ({ path, component: Component, permissions, exact, to }) => {
  const { isSuperuser, permissionsList } = useSelector(
    (state) => ({
      isSuperuser: getSuperuserKeyFromJwt(state.auth.authToken),
      permissionsList: state.auth.permissions,
    })
  );

  const isAllowedPermission = !permissions.length || permissions.some(permission => permissionsList.includes(permission));

  return (
    <Route
      exact={exact}
      path={path}
      render={() =>
        (isSuperuser || isAllowedPermission) ? (
          <Component />
        ) : (
          <Redirect to={to} />
        )
      }
    />
  );
};

PermissionsRoute.propTypes = propTypes;
PermissionsRoute.defaultProps = defaultProps;
