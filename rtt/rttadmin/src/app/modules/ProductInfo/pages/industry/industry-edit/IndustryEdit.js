/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import React, { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { shallowEqual, useSelector } from "react-redux";
import * as actions from "@redux-product/industry/industryActions";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { IndustryEditForm } from "./IndustryEditForm";
import { useSubheader } from "@metronic/layout";
import { ModalProgressBar } from "@metronic-partials/controls";

const initIndustry = {
  id: undefined,
  name: "",
  description: "",
};

export function IndustryEdit({
  history,
  match: {
    params: { id },
  },
}) {
  // Subheader
  const suhbeader = useSubheader();

  // Tabs
  const [title, setTitle] = useState("");
  const dispatch = useDispatch();

  const { actionsLoading, industryForEdit } = useSelector(
    (state) => ({
      actionsLoading: state.industry.actionsLoading,
      industryForEdit: state.industry.industryForEdit,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.fetchIndustry(id));
  }, [id, dispatch]);

  useEffect(() => {
    let _title = id ? "" : "Create Industry";
    if (industryForEdit && id) {
      _title = `Edit industry '${industryForEdit.name}'`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [industryForEdit, id]);

  const saveIndustry = (values) => {
    if (!id) {
      dispatch(actions.createIndustry(values)).then(() => backToIndustryList());
    } else {
      dispatch(actions.updateIndustry(values)).then(() => backToIndustryList());
    }
  };

  const btnRef = useRef();
  const saveIndustryClick = () => {
    if (btnRef && btnRef.current) {
      btnRef.current.click();
    }
  };

  const backToIndustryList = () => {
    history.push(`/backend/product-info/industries`);
  };

  return (
    <Card>
      {actionsLoading && <ModalProgressBar />}
      <CardHeader title={title}>
        <CardHeaderToolbar>
          <button
            type="button"
            onClick={backToIndustryList}
            className="btn btn-light"
          >
            <i className="fa fa-arrow-left"></i>
            Back
          </button>
          {`  `}
          <button
            type="submit"
            className="btn btn-primary ml-2"
            onClick={saveIndustryClick}
          >
            Save
          </button>
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <div className="mt-5">
          <IndustryEditForm
            actionsLoading={actionsLoading}
            industry={industryForEdit || initIndustry}
            btnRef={btnRef}
            saveIndustry={saveIndustry}
          />
        </div>
      </CardBody>
    </Card>
  );
}
