/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import React, { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { shallowEqual, useSelector } from "react-redux";
import * as actions from "@redux-regulation/impact-assessment/impactAssessmentActions";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { ImpactAssessmentSelectForm } from "./ImpactAssessmentSelectForm";
import { useSubheader } from "@metronic/layout";
import { ModalProgressBar } from "@metronic-partials/controls";

const initImpactAssessment = {
  id: undefined,
  name: "",
  region: "",
  description: "",
};
export function ImpactAssessmentSelect({
  history,
  match: {
    params: { id },
  },
}) {
  // Subheader
  const suhbeader = useSubheader();

  const [title, setTitle] = useState("");
  const dispatch = useDispatch();

  const { actionsLoading, impactAssessmentForSelect } = useSelector(
    (state) => ({
      actionsLoading: state.impactAssessment.actionsLoading,
      impactAssessmentForSelect:
        state.impactAssessment.impactAssessmentForSelect,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.selectImpactAssessment(id));
  }, [id, dispatch]);

  useEffect(() => {
    let _title = id ? "" : "Create ImpactAssessment";
    if (impactAssessmentForSelect && id) {
      _title = `Select impactAssessment: ${impactAssessmentForSelect.name}`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [impactAssessmentForSelect, id]);

  const backToImpactAssessmentList = () => {
    history.push(`/backend/regulation-info/impactAssessment`);
  };

  return (
    <Card>
      {actionsLoading && <ModalProgressBar />}
      <CardHeader title={title}>
        <CardHeaderToolbar>
          <button
            type="button"
            onClick={backToImpactAssessmentList}
            className="btn btn-light"
          >
            <i className="fa fa-arrow-left"></i>
            Back
          </button>
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <div className="mt-5">
          <ImpactAssessmentSelectForm
            actionsLoading={actionsLoading}
            impactAssessment={impactAssessmentForSelect || initImpactAssessment}
          />
        </div>
      </CardBody>
    </Card>
  );
}
