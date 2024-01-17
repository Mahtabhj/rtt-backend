/* eslint-disable jsx-a11y/anchor-is-valid */
import React from "react";
import { Link, Switch, Redirect } from "react-router-dom";
import { toAbsoluteUrl } from "@metronic-helpers";
import { ContentRoute } from "@metronic/layout";
import Login from "./Login";
import Registration from "./Registration";
import ForgotPassword from "./ForgotPassword";
import "@metronic-assets/sass/pages/login/classic/login-1.scss";

export function AuthPage() {
  const currentYearString = (new Date().getFullYear()).toString();

  return (
    <div className="d-flex flex-column flex-root">
      <div
        className="login login-1 login-signin-on d-flex flex-column flex-lg-row flex-row-fluid bg-white"
        id="kt_login"
      >
        <div
          className="login-aside d-flex flex-row-auto bgi-size-cover bgi-no-repeat p-10 p-lg-10"
          style={{
            backgroundImage: `url(${toAbsoluteUrl(
              process.env.REACT_APP_STATIC_PATH + "/bg/bg-1.jpg"
            )})`,
          }}
        >
          <div className="d-flex flex-row-fluid flex-column justify-content-between">
            <Link to="/backend/backend/" className="flex-column-auto position-relative min-h-70px">
              <img
                alt="Logo"
                className="max-h-100px"
                src={toAbsoluteUrl(
                  process.env.REACT_APP_STATIC_PATH +
                  "/logos/brand-logo.svg"
                )}
              />
            </Link>

            <div className="flex-column-fluid d-flex flex-column justify-content-center">
              <h3 className="font-size-h1 mb-5 text-white">
                Welcome to ProductComply Admin!
              </h3>
            </div>

            <div className="d-none flex-column-auto d-lg-flex justify-content-between mt-10">
              <div className="opacity-70 font-weight-bold	text-white">
                &copy; {currentYearString} ProductComply
              </div>
            </div>
          </div>
        </div>

        <div className="flex-row-fluid d-flex flex-column position-relative p-7 overflow-hidden">
          <div className="position-absolute top-0 right-0 text-right mt-5 mb-15 mb-lg-0 flex-column-auto justify-content-center py-5 px-10">
          </div>

          <div className="d-flex flex-column-fluid flex-center mt-30 mt-lg-0">
            <Switch>
              <ContentRoute path="/backend/auth/login" component={Login} />
              <ContentRoute
                path="/backend/auth/registration"
                component={Registration}
              />
              <ContentRoute
                path="/backend/auth/forgot-password"
                component={ForgotPassword}
              />
              <Redirect
                from="/backend/auth"
                exact={true}
                to="/backend/auth/login"
              />
              <Redirect to="/backend/auth/login" />
            </Switch>
          </div>

          <div className="d-flex d-lg-none flex-column-auto flex-column flex-sm-row justify-content-between align-items-center mt-5 p-5">
            <div className="text-dark-50 font-weight-bold order-2 order-sm-1 my-2">
              &copy; {currentYearString} ProductComply
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
