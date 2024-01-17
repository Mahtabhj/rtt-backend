/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
  ModalProgressBar,
} from "@metronic-partials/controls";
import { useSubheader } from "@metronic/layout";
import * as actions from "@redux-news/source/sourceActions";
import React, { useEffect, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { SourceSelectForm } from "./SourceSelectForm";

const initSource = {
  id: undefined,
  name: "",
  link: "",
  description: "",
};
export function SourceSelect({
  history,
  match: {
    params: { id },
  },
}) {
  // Subheader
  const suhbeader = useSubheader();

  const [title, setTitle] = useState("");
  const dispatch = useDispatch();

  const { actionsLoading, sourceForSelect } = useSelector(
    (state) => ({
      actionsLoading: state.source.actionsLoading,
      sourceForSelect: state.source.sourceForSelect,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.selectSource(id));
  }, [id, dispatch]);

  useEffect(() => {
    let _title = id ? "" : "Create Source";
    if (sourceForSelect && id) {
      _title = `Select source : ${sourceForSelect.title}`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sourceForSelect, id]);

  const backToSourceList = () => {
    history.push(`/backend/news-info/sources`);
  };

  return (
    <Card>
      {actionsLoading && <ModalProgressBar />}
      <CardHeader title={title}>
        <CardHeaderToolbar>
          <button
            type="button"
            onClick={backToSourceList}
            className="btn btn-light"
          >
            <i className="fa fa-arrow-left"></i>
            Back
          </button>
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <div className="mt-5">
          <SourceSelectForm
            actionsLoading={actionsLoading}
            source={sourceForSelect || initSource}
          />
        </div>
      </CardBody>
    </Card>
  );
}
