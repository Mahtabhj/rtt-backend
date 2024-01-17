/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
  ModalProgressBar,
} from "@metronic-partials/controls";
import { useSubheader } from "@metronic/layout";
import * as actions from "@redux-document/document/documentActions";
import React, { useEffect, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { DocumentSelectForm } from "./DocumentSelectForm";

const initDocument = {
  id: undefined,
  title: "",
  type: "",
  description: "",
};
export function DocumentSelect({
  history,
  match: {
    params: { id },
  },
}) {
  // Subheader
  const suhbeader = useSubheader();

  const [title, setTitle] = useState("");
  const dispatch = useDispatch();

  const { actionsLoading, documentForSelect } = useSelector(
    (state) => ({
      actionsLoading: state.document.actionsLoading,
      documentForSelect: state.document.documentForSelect,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.selectDocument(id));
  }, [id, dispatch]);

  useEffect(() => {
    let _title = id ? "" : "Create Document";
    if (documentForSelect && id) {
      _title = `Select document : ${documentForSelect.title}`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [documentForSelect, id]);

  const backToDocumentList = () => {
    history.push(`/backend/document-info/documents`);
  };

  return (
    <Card>
      {actionsLoading && <ModalProgressBar />}
      <CardHeader title={title}>
        <CardHeaderToolbar>
          <button
            type="button"
            onClick={backToDocumentList}
            className="btn btn-light"
          >
            <i className="fa fa-arrow-left"></i>
            Back
          </button>
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <div className="mt-5">
          <DocumentSelectForm
            actionsLoading={actionsLoading}
            document={documentForSelect || initDocument}
          />
        </div>
      </CardBody>
    </Card>
  );
}
