import React from "react";
import { useSelector } from "react-redux";
import { Redirect, Route } from "react-router-dom";

import { getSuperuserKeyFromJwt } from "../../../../app/common";

import { Content } from "./Content";

export function ContentRoute({ children, component, render, permission, to, ...props }) {
  const { isSuperuser, permissionsList } = useSelector(
    (state) => ({
      isSuperuser: getSuperuserKeyFromJwt(state.auth.authToken),
      permissionsList: state.auth.permissions,
    })
  );

  const isAllowedPermission = !permission || isSuperuser || permissionsList.includes(permission);

  return (
    <Route {...props}>
      {routeProps => {
        if (typeof children === "function") {
          return <Content>{children(routeProps)}</Content>;
        }

        if (!routeProps.match || !isAllowedPermission) {
          return to ? <Redirect to={to} /> : null;
        }

        if (children) {
          return <Content>{children}</Content>;
        }

        if (component) {
          return (
            <Content>{React.createElement(component, routeProps)}</Content>
          );
        }

        if (render) {
          return <Content>{render(routeProps)}</Content>;
        }

        return null;
      }}
    </Route>
  );
}
