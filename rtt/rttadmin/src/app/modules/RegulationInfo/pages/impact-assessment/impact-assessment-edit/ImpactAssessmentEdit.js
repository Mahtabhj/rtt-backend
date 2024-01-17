/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
  ModalProgressBar,
} from "@metronic-partials/controls";
import { useSubheader } from "@metronic/layout";
import * as actions from "@redux-regulation/impact-assessment/impactAssessmentActions";
import { fetchRegulationList } from "@redux-regulation/regulation/regulationActions";
import React, { useEffect, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { SingleImpactAssessmentTable } from "../single-impact-assessment/SingleImpactAssessmentTable";

export function ImpactAssessmentEdit({
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

  const { actionsLoading, impactAssessments } = useSelector(
    (state) => ({
      actionsLoading: state.impactAssessment.actionsLoading,
      impactAssessments: state.impactAssessment.entities,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(fetchRegulationList());
    dispatch(actions.fetchImpactAssessmentAnswers());
    dispatch(actions.fetchUserList());
  }, [id, dispatch]);

  useEffect(() => {
    let _title = "";
    if (impactAssessments && impactAssessments[id - 1] && id) {
      _title =
        impactAssessments &&
        `Impact Assessment for: ${
          impactAssessments[id - 1].regulation.regulation_name
        }`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [impactAssessments && impactAssessments[id - 1], id]);

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
          <SingleImpactAssessmentTable
            impactAssessmentId={id - 1}
            actionsLoading={actionsLoading}
          />
        </div>
      </CardBody>
    </Card>
  );
}
