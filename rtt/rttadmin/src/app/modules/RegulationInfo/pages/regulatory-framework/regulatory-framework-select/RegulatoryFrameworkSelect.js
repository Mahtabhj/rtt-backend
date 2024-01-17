/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
  ModalProgressBar,
} from "@metronic-partials/controls";
import { useSubheader } from "@metronic/layout";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import React, { useEffect, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { RegulatoryFrameworkSelectForm } from "./RegulatoryFrameworkSelectForm";

const initRegulatoryFramework = {
  id: undefined,
  name: "",
  review_status: "",
  status: "",
  description: "",
  issuing_body: "",
  regions: "",
  documents: "",
  material_categories: "",
  product_categories: "",
  urls: "",
};
export function RegulatoryFrameworkSelect({
  history,
  match: {
    params: { id },
  },
}) {
  // Subheader
  const suhbeader = useSubheader();

  const [title, setTitle] = useState("");
  const dispatch = useDispatch();

  const { actionsLoading, regulatoryFrameworkForSelect } = useSelector(
    (state) => ({
      actionsLoading: state.regulatoryFramework.actionsLoading,
      regulatoryFrameworkForSelect:
        state.regulatoryFramework.regulatoryFrameworkForSelect,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.selectRegulatoryFramework(id));
  }, [id, dispatch]);

  useEffect(() => {
    let _title = id ? "" : "Create RegulatoryFramework";
    if (regulatoryFrameworkForSelect && id) {
      _title = `Select regulatoryFramework : ${regulatoryFrameworkForSelect.name}`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [regulatoryFrameworkForSelect, id]);

  const backToRegulatoryFrameworkList = () => {
    history.push(`/backend/regulation-info/regulatory-framework`);
  };

  return (
    <Card>
      {actionsLoading && <ModalProgressBar />}
      <CardHeader title={title}>
        <CardHeaderToolbar>
          <button
            type="button"
            onClick={backToRegulatoryFrameworkList}
            className="btn btn-light"
          >
            <i className="fa fa-arrow-left"></i>
            Back
          </button>
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <div className="mt-5">
          <RegulatoryFrameworkSelectForm
            actionsLoading={actionsLoading}
            regulatoryFramework={
              regulatoryFrameworkForSelect || initRegulatoryFramework
            }
          />
        </div>
      </CardBody>
    </Card>
  );
}
