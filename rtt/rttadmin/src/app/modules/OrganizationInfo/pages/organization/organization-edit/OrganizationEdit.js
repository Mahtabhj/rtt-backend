/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import React, { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { shallowEqual, useSelector } from "react-redux";
import * as actions from "@redux-organization/organization/organizationActions";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { OrganizationEditForm } from "./OrganizationEditForm";
import { useSubheader } from "@metronic/layout";
import { ModalProgressBar } from "@metronic-partials/controls";
import { UsersTable } from "../users-table/UsersTable";
import { SubscriptionsTable } from "../subscriptions-table/SubscriptionsTable";

const initOrganization = {
  id: undefined,
  name: "",
  country: "",
  address: "",
  tax_code: "",
  active: true,
  description: "",
  primary_color: "",
  secondary_color: "",
  session_timeout: 0,
  password_expiration: 0,
  logo: "",
};

export function OrganizationEdit({
  history,
  match: {
    params: { id },
  },
}) {
  // Subheader
  const suhbeader = useSubheader();

  // Tabs
  const [tab, setTab] = useState("users");
  const [title, setTitle] = useState("");
  const dispatch = useDispatch();

  const { actionsLoading, organizationForEdit, success } = useSelector(
    (state) => ({
      actionsLoading: state.organization.actionsLoading,
      organizationForEdit: state.organization.organizationForEdit,
      success: state.organization.success,
    }),
    shallowEqual
  );

  useEffect(() => {
    if (success === 'organization') {
      backToOrganizationList()
    }
  }, [success]);

  useEffect(() => {
    dispatch(actions.fetchOrganization(id));
  }, [id, dispatch]);

  useEffect(() => {
    let _title = id ? "" : "Create Organization";
    if (organizationForEdit && id) {
      _title = `Edit organization '${organizationForEdit.name}'`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [organizationForEdit, id]);

  const saveOrganization = (values) => {
    if (!id) {
      dispatch(actions.createOrganization(values))
    } else {
      dispatch(actions.updateOrganization(values));
    }
  };

  const btnRef = useRef();
  const saveOrganizationClick = () => {
    if (btnRef && btnRef.current) {
      btnRef.current.click();
    }
  };

  const backToOrganizationList = () => {
    history.push(`/backend/organization-info/organizations`);
  };

  return (
    <>
      <Card>
        {actionsLoading && <ModalProgressBar />}
        <CardHeader title={title}>
          <CardHeaderToolbar>
            <button
              type="button"
              onClick={backToOrganizationList}
              className="btn btn-light"
            >
              <i className="fa fa-arrow-left"></i>
              Back
            </button>
            {`  `}
            <button
              type="submit"
              className="btn btn-primary ml-2"
              onClick={saveOrganizationClick}
            >
              Save
            </button>
          </CardHeaderToolbar>
        </CardHeader>
        <CardBody>
          <OrganizationEditForm
            actionsLoading={actionsLoading}
            organization={organizationForEdit || initOrganization}
            btnRef={btnRef}
            saveOrganization={saveOrganization}
          />
        </CardBody>
      </Card>

      {id && (
        <Card>
          <CardBody>
            <ul className="nav nav-tabs nav-tabs-line " role="tablist">
              <li className="nav-item" onClick={() => setTab("users")}>
                <a
                  className={`nav-link ${tab === "users" && "active"}`}
                  data-toggle="tab"
                  role="button"
                  aria-selected={(tab === "users").toString()}
                >
                  Users
                </a>
              </li>
              <li className="nav-item" onClick={() => setTab("subscriptions")}>
                <a
                  className={`nav-link ${tab === "subscriptions" && "active"}`}
                  data-toggle="tab"
                  role="tab"
                  aria-selected={(tab === "subscriptions").toString()}
                >
                  Subscriptions
                </a>
              </li>
            </ul>
            <div className="mt-5">
              {tab === "users" && id && (
                <UsersTable history={history} organizationId={id} />
              )}
              {tab === "subscriptions" && id && (
                <SubscriptionsTable history={history} organizationId={id} />
              )}
            </div>
          </CardBody>
        </Card>
      )}
    </>
  );
}
