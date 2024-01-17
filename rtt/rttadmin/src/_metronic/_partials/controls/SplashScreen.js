import React from "react";
import {CircularProgress} from "@material-ui/core";
import {toAbsoluteUrl} from "@metronic-helpers";

export function SplashScreen() {
  return (
    <div className="splash-screen">
      <img
        src={toAbsoluteUrl(process.env.REACT_APP_STATIC_PATH + "/media/logos/brand-logo.svg")}
        alt="ProductComply Admin logo"
      />
      <CircularProgress className="splash-screen-spinner" />
    </div>
  );
}
