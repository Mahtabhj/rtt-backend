/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid */
import React from "react";
import { NavLink, useLocation } from "react-router-dom";
import SVG from "react-inlinesvg";

import { toAbsoluteUrl, checkIsActive } from "@metronic-helpers";

import { AuthorizeDocument, AuthorizeRegulation } from "@common/Permissions/AuthorizeWrappers";
import { PermissionsWrapper } from "@common/Permissions/PermissionsWrapper";
import {
  ANSWER,
  EXEMPTION,
  FRAMEWORK_PERMISSION,
  INDUSTRY,
  ISSUING_BODY,
  LIMIT_PERMISSION,
  MATERIAL_CATEGORY,
  NEWS,
  NEWS_ASSESSMENT_WORKFLOW,
  ORGANIZATION, PRODUCT_CATEGORY,
  REGULATION,
  SOURCE,
  SUBSTANCE,
  SUBSTANCE_FAMILY,
  USER,
  REGION
} from "@common";

export function AsideMenuList({ layoutProps }) {
  const location = useLocation();

  const getMenuItemActive = (url, hasSubmenu = false) =>
    checkIsActive(location, url) ? `${!hasSubmenu && 'menu-item-active'} menu-item-open` : '';

  return (
    <>
      <ul className={`menu-nav ${layoutProps.ulClasses}`}>
        <li
          className={`menu-item ${getMenuItemActive(
            "/backend/dashboard",
            false
          )}`}
          aria-haspopup="true"
        >
          <NavLink className="menu-link" to="/backend/dashboard">
            <span className="svg-icon menu-icon">
              <SVG
                src={toAbsoluteUrl(
                  process.env.REACT_APP_STATIC_PATH +
                    "/svg/icons/Design/Layers.svg"
                )}
              />
            </span>
            <span className="menu-text">Dashboard</span>
          </NavLink>
        </li>

        <li className="menu-section ">
          <h4 className="menu-text">Modules</h4>
        </li>

        {/* Organization Module Menu */}
        <PermissionsWrapper permissions={[ORGANIZATION, USER]}>
          <li
            className={`menu-item menu-item-submenu ${getMenuItemActive(
              "/backend/organization-info",
              true
            )}`}
            aria-haspopup="true"
            data-menu-toggle="hover"
          >
            <NavLink
              className="menu-link menu-toggle"
              to="/backend/organization-info"
            >
              <span className="svg-icon menu-icon">
                <SVG
                  src={toAbsoluteUrl(
                    process.env.REACT_APP_STATIC_PATH +
                      "/svg/icons/Shopping/Box2.svg"
                  )}
                />
              </span>
              <span className="menu-text">Organization</span>
              <i className="menu-arrow" />
            </NavLink>
            <div className="menu-submenu">
              <i className="menu-arrow" />
              <ul className="menu-subnav">
                <PermissionsWrapper permissions={[ORGANIZATION]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/organization-info/organizations"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/organization-info/organizations"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Organizations</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>

                <PermissionsWrapper permissions={[USER]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/organization-info/users"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/organization-info/users"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Users</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>
              </ul>
            </div>
          </li>
        </PermissionsWrapper>

        {/* News Module Menu */}
        <PermissionsWrapper permissions={[NEWS, NEWS_ASSESSMENT_WORKFLOW, SOURCE]}>
          <li
            className={`menu-item menu-item-submenu ${getMenuItemActive(
              "/backend/news-info",
              true
            )}`}
            aria-haspopup="true"
            data-menu-toggle="hover"
          >
            <NavLink className="menu-link menu-toggle" to="/backend/news-info">
              <span className="svg-icon menu-icon">
                <SVG
                  src={toAbsoluteUrl(
                    process.env.REACT_APP_STATIC_PATH +
                      "/svg/icons/Shopping/Box1.svg"
                  )}
                />
              </span>
              <span className="menu-text">News</span>
              <i className="menu-arrow" />
            </NavLink>
            <div className="menu-submenu">
              <i className="menu-arrow" />
              <ul className="menu-subnav">
                <PermissionsWrapper permissions={[NEWS]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/news-info/news"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink className="menu-link" to="/backend/news-info/news">
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Select news</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>

                <PermissionsWrapper permissions={[NEWS_ASSESSMENT_WORKFLOW]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/news-info/impactAssessment"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink className="menu-link" to="/backend/news-info/impactAssessment">
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Impact assessment</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>

                <PermissionsWrapper permissions={[SOURCE]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/news-info/sources"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink className="menu-link" to="/backend/news-info/sources">
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Source</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>
              </ul>
            </div>
          </li>
        </PermissionsWrapper>

        {/* Regulation Module Menu */}
        <PermissionsWrapper permissions={[FRAMEWORK_PERMISSION, REGULATION, ISSUING_BODY, ANSWER]}>
          <li
            className={`menu-item menu-item-submenu ${getMenuItemActive(
              "/backend/regulation-info",
              true
            )}`}
            aria-haspopup="true"
            data-menu-toggle="hover"
          >
            <NavLink
              className="menu-link menu-toggle"
              to="/backend/regulation-info"
            >
              <span className="svg-icon menu-icon">
                <SVG
                  src={toAbsoluteUrl(
                    process.env.REACT_APP_STATIC_PATH +
                      "/svg/icons/Code/Info-circle.svg"
                  )}
                />
              </span>
              <span className="menu-text">Regulation</span>
              <i className="menu-arrow" />
            </NavLink>
            <div className="menu-submenu">
              <i className="menu-arrow" />
              <ul className="menu-subnav">
                <PermissionsWrapper permissions={[FRAMEWORK_PERMISSION]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/regulation-info/regulatory-framework"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/regulation-info/regulatory-framework"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Regulatory Framework</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>

                <AuthorizeRegulation>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/regulation-info/regulation"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/regulation-info/regulation"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Regulation</span>
                    </NavLink>
                  </li>
                </AuthorizeRegulation>

                <PermissionsWrapper permissions={[ISSUING_BODY]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/regulation-info/issuingbody"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/regulation-info/issuingbody"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Issuing Body</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>

                <PermissionsWrapper permissions={[ANSWER]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/regulation-info/impactAssessment"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/regulation-info/impactAssessment"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Impact Assessment</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>
              </ul>
            </div>
          </li>
        </PermissionsWrapper>

        {/* Substances Module Menu */}
        <PermissionsWrapper permissions={[SUBSTANCE, SUBSTANCE_FAMILY]}>
          <li
            className={`menu-item menu-item-submenu ${getMenuItemActive(
              "/backend/substance-info",
              true
            )}`}
            aria-haspopup="true"
            data-menu-toggle="hover"
          >
            <NavLink
              className="menu-link menu-toggle"
              to="/backend/substance-info"
            >
            <span className="svg-icon menu-icon">
              <SVG
                src={toAbsoluteUrl(
                  process.env.REACT_APP_STATIC_PATH +
                  "/svg/icons/General/Flask.svg"
                )}
              />
            </span>
              <span className="menu-text">Substance</span>
              <i className="menu-arrow" />
            </NavLink>
            <div className="menu-submenu">
              <ul className="menu-subnav">
                <PermissionsWrapper permissions={[SUBSTANCE]}>
                  <li
                    className={`menu-item ${getMenuItemActive("/backend/substance-info/substance")}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/substance-info/substance"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Substance data</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>

                <PermissionsWrapper permissions={[SUBSTANCE_FAMILY]}>
                  <li
                    className={`menu-item ${getMenuItemActive("/backend/substance-info/family")}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/substance-info/family"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Family</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>
              </ul>
            </div>
          </li>
        </PermissionsWrapper>

        {/* Limits Module Menu */}
        <PermissionsWrapper permissions={[LIMIT_PERMISSION, EXEMPTION]}>
          <li
            className={`menu-item menu-item-submenu ${getMenuItemActive(
              "/backend/limit-info",
              true
            )}`}
            aria-haspopup="true"
            data-menu-toggle="hover"
          >
            <NavLink
              className="menu-link menu-toggle"
              to="/backend/limit-info"
            >
            <span className="svg-icon menu-icon">
              <SVG
                src={toAbsoluteUrl(
                  process.env.REACT_APP_STATIC_PATH +
                  "/svg/icons/General/Scale.svg"
                )}
              />
            </span>
              <span className="menu-text">Limit</span>
              <i className="menu-arrow" />
            </NavLink>
            <div className="menu-submenu">
              <ul className="menu-subnav">
                <PermissionsWrapper permissions={[LIMIT_PERMISSION]}>
                  <li
                    className={`menu-item ${getMenuItemActive("/backend/limit-info/limit")}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/limit-info/limit"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Limit</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>

                <PermissionsWrapper permissions={[EXEMPTION]}>
                  <li
                    className={`menu-item ${getMenuItemActive("/backend/limit-info/exemption")}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/limit-info/exemption"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Exemption</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>
              </ul>
            </div>
          </li>
        </PermissionsWrapper>

        {/* Product Module Menu */}
        <PermissionsWrapper permissions={[INDUSTRY, PRODUCT_CATEGORY, MATERIAL_CATEGORY]}>
          <li
            className={`menu-item menu-item-submenu ${getMenuItemActive(
              "/backend/product-info",
              true
            )}`}
            aria-haspopup="true"
            data-menu-toggle="hover"
          >
            <NavLink className="menu-link menu-toggle" to="/product-info">
              <span className="svg-icon menu-icon">
                <SVG
                  src={toAbsoluteUrl(
                    process.env.REACT_APP_STATIC_PATH +
                      "/svg/icons/Shopping/Cart1.svg"
                  )}
                />
              </span>
              <span className="menu-text">Product</span>
              <i className="menu-arrow" />
            </NavLink>
            <div className="menu-submenu">
              <i className="menu-arrow" />
              <ul className="menu-subnav">
                <PermissionsWrapper permissions={[INDUSTRY]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/product-info/industries"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/product-info/industries"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Industries</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>

                <PermissionsWrapper permissions={[PRODUCT_CATEGORY]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/product-info/product-categories"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/product-info/product-categories"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Product Categories</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>

                <PermissionsWrapper permissions={[MATERIAL_CATEGORY]}>
                  <li
                    className={`menu-item ${getMenuItemActive(
                      "/backend/product-info/material-categories"
                    )}`}
                    aria-haspopup="true"
                  >
                    <NavLink
                      className="menu-link"
                      to="/backend/product-info/material-categories"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Material Categories</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>
              </ul>
            </div>
          </li>
        </PermissionsWrapper>

        {/* Document Module Menu */}
        <AuthorizeDocument>
          <li
            className={`menu-item menu-item-submenu ${getMenuItemActive(
              "/backend/document-info",
              true
            )}`}
            aria-haspopup="true"
            data-menu-toggle="hover"
          >
            <NavLink
              className="menu-link menu-toggle"
              to="/backend/document-info"
            >
              <span className="svg-icon menu-icon">
                <SVG
                  src={toAbsoluteUrl(
                    process.env.REACT_APP_STATIC_PATH +
                      "/svg/icons/Shopping/Wallet2.svg"
                  )}
                />
              </span>
              <span className="menu-text">Document</span>
              <i className="menu-arrow" />
            </NavLink>
            <div className="menu-submenu">
              <i className="menu-arrow" />
              <ul className="menu-subnav">
                <li className="menu-item menu-item-parent" aria-haspopup="true">
                  <span className="menu-link">
                    <span className="menu-text">Document</span>
                  </span>
                </li>

                <li
                  className={`menu-item ${getMenuItemActive(
                    "/backend/document-info/documents"
                  )}`}
                  aria-haspopup="true"
                >
                  <NavLink
                    className="menu-link"
                    to="/backend/document-info/documents"
                  >
                    <i className="menu-bullet menu-bullet-dot">
                      <span />
                    </i>
                    <span className="menu-text">Documents</span>
                  </NavLink>
                </li>
              </ul>
            </div>
          </li>
        </AuthorizeDocument>

        {/*Region Module Menu*/}
        <PermissionsWrapper permissions={[REGION]}>
          <li
              className={`menu-item menu-item-submenu ${getMenuItemActive(
                  "/backend/region-info",
                  true
              )}`}
              aria-haspopup="true"
              data-menu-toggle="hover"
          >
            <NavLink
                className="menu-link menu-toggle"
                to="/backend/region-info"
            >
            <span className="svg-icon menu-icon">
              <SVG
                  src={toAbsoluteUrl(
                      process.env.REACT_APP_STATIC_PATH +
                      "/svg/icons/Region/Earth.svg"
                  )}
              />
            </span>
              <span className="menu-text">Region</span>
              <i className="menu-arrow" />
            </NavLink>
            <div className="menu-submenu">
              <ul className="menu-subnav">
                <PermissionsWrapper permissions={[REGION]}>
                  <li
                      className={`menu-item ${getMenuItemActive("/backend/region-info/region")}`}
                      aria-haspopup="true"
                  >
                    <NavLink
                        className="menu-link"
                        to="/backend/region-info/region"
                    >
                      <i className="menu-bullet menu-bullet-dot">
                        <span />
                      </i>
                      <span className="menu-text">Region Page</span>
                    </NavLink>
                  </li>
                </PermissionsWrapper>
              </ul>
            </div>
          </li>
        </PermissionsWrapper>
      </ul>
    </>
  );
}
