/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
  ModalProgressBar,
} from "@metronic-partials/controls";
import { useSubheader } from "@metronic/layout";
import * as actions from "@redux-regulation/issuingbody/issuingbodyActions";
import React, { useEffect, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { IssuingBodySelectForm } from "./IssuingBodySelectForm";

const initIssuingBody = {
  id: undefined,
  name: "",
  region: "",
  description: "",
};
export function IssuingBodySelect({
  history,
  match: {
    params: { id },
  },
}) {
  // Subheader
  const suhbeader = useSubheader();

  const [title, setTitle] = useState("");
  const dispatch = useDispatch();

  const { actionsLoading, issuingbodyForSelect } = useSelector(
    (state) => ({
      actionsLoading: state.issuingbody.actionsLoading,
      issuingbodyForSelect: state.issuingbody.issuingbodyForSelect,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.selectIssuingBody(id));
  }, [id, dispatch]);

  useEffect(() => {
    let _title = id ? "" : "Create Issuing Body";
    if (issuingbodyForSelect && id) {
      _title = `Select issuingbody: ${issuingbodyForSelect.name}`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [issuingbodyForSelect, id]);

  const backToIssuingBodyList = () => {
    history.push(`/backend/regulation-info/issuingbody`);
  };

  return (
    <Card>
      {actionsLoading && <ModalProgressBar />}
      <CardHeader title={title}>
        <CardHeaderToolbar>
          <button
            type="button"
            onClick={backToIssuingBodyList}
            className="btn btn-light"
          >
            <i className="fa fa-arrow-left"></i>
            Back
          </button>
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <div className="mt-5">
          <IssuingBodySelectForm
            actionsLoading={actionsLoading}
            issuingbody={issuingbodyForSelect || initIssuingBody}
          />
        </div>
      </CardBody>
    </Card>
  );
}
