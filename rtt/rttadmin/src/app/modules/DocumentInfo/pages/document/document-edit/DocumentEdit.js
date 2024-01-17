/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import React, { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { shallowEqual, useSelector } from "react-redux";
import * as actions from "@redux-document/document/documentActions";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { DocumentEditForm } from "./DocumentEditForm";
import { useSubheader } from "@metronic/layout";
import { ModalProgressBar } from "@metronic-partials/controls";

export function DocumentEdit({
  history,
  match: {
    params: { id },
  },
}) {
  // Subheader
  const suhbeader = useSubheader();

  const [initDocument, setinitDocument] = useState({
    id: undefined,
    title: "",
    type: "",
    description: "",
  });

  // Tabs
  const [tab, setTab] = useState("basic");
  const [title, setTitle] = useState("");
  const dispatch = useDispatch();

  const { actionsLoading, documentForEdit } = useSelector(
    (state) => ({
      actionsLoading: state.document.actionsLoading,
      documentForEdit: state.document.documentForEdit,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.fetchDocument(id));
    dispatch(actions.fetchDocumentTypeList());
  }, [id, dispatch]);

  useEffect(() => {
    let _title = id ? "" : "Create Document";
    if (documentForEdit && id) {
      _title = `Edit document: ${documentForEdit.title}`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [documentForEdit, id]);

  const { documentTypeList } = useSelector(
    (state) => ({
      documentTypeList: state.document.documentTypeList,
    }),
    shallowEqual
  );

  useEffect(() => {
    if (!id && documentTypeList) {
      let newInit = {
        ...initDocument,
        type: documentTypeList.length > 0 ? documentTypeList[0].id : null,
      };
      setinitDocument(newInit);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, documentTypeList]);

  const saveDocument = (values) => {
    if (!id) {
      dispatch(actions.createDocument(values)).then(() => backToDocumentList());
    } else {
      dispatch(actions.updateDocument(values)).then(() => backToDocumentList());
    }
  };

  const btnRef = useRef();
  const saveDocumentClick = () => {
    if (btnRef && btnRef.current) {
      btnRef.current.click();
    }
  };

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
          
          {`  `}
          <button
            type="submit"
            className="btn btn-primary ml-2"
            onClick={saveDocumentClick}
          >
            Save
          </button>
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <ul className="nav nav-tabs nav-tabs-line " role="tablist">
          <li className="nav-item" onClick={() => setTab("basic")}>
            <a
              className={`nav-link ${tab === "basic" && "active"}`}
              data-toggle="tab"
              role="tab"
              aria-selected={(tab === "basic").toString()}
            >
              Basic info
            </a>
          </li>
        </ul>
        <div className="mt-5">
          {tab === "basic" && (
            <DocumentEditForm
              actionsLoading={actionsLoading}
              document={documentForEdit || initDocument}
              btnRef={btnRef}
              saveDocument={saveDocument}
              documentTypeList={documentTypeList || []}
            />
          )}
        </div>
      </CardBody>
    </Card>
  );
}
