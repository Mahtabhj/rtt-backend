/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import React, { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { shallowEqual, useSelector } from "react-redux";
import * as actions from "@redux-news/source/sourceActions";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { SourceEditForm } from "./SourceEditForm";
import { useSubheader } from "@metronic/layout";
import { ModalProgressBar } from "@metronic-partials/controls";


export function SourceEdit({
  history,
  match: {
    params: { id },
  },
}) {
  const [initSource, setinitSource] = useState({
    id: undefined,
    name: "",
    link: "",
    description: "",
    type: "",
    image: "",
  });
  // Subheader
  const suhbeader = useSubheader();

  // Tabs
  const [tab, setTab] = useState("basic");
  const [title, setTitle] = useState("");
  const dispatch = useDispatch();

  const { actionsLoading, sourceForEdit, sourceType } = useSelector(
    (state) => ({
      actionsLoading: state.source.actionsLoading,
      sourceForEdit: state.source.sourceForEdit,
      sourceType: state.source.sourceType,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.fetchSource(id));
    dispatch(actions.fetchSourceTypeList());
  }, [id, dispatch]);

  useEffect(() => {
    let _title = id ? "" : "Create Source";
    if (sourceForEdit && id) {
      _title = `Edit source: ${sourceForEdit.name}`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sourceForEdit, id]);

  useEffect(() => {
    if (!id && sourceType) {
      let newInit = {
        ...initSource,
        type: sourceType.length > 0 ? sourceType[0].id : null,
      };
      setinitSource(newInit);
    } else if (id && sourceForEdit) {
      let newInit = {
        ...sourceForEdit,
        type: sourceForEdit.type ? sourceForEdit.type.id : (sourceType ? sourceType[0].id : null),
      };
      setinitSource(newInit);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sourceType, sourceForEdit, id]);

  const saveSource = (values) => {
    if (!id) {
      dispatch(actions.createSource(values)).then(() => backToSourceList());
    } else {
      dispatch(actions.updateSource(values)).then(() => backToSourceList());
    }
  };

  const btnRef = useRef();
  const saveSourceClick = () => {
    if (btnRef && btnRef.current) {
      btnRef.current.click();
    }
  };

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

          {`  `}
          <button
            type="submit"
            className="btn btn-primary ml-2"
            onClick={saveSourceClick}
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
            <SourceEditForm
              actionsLoading={actionsLoading}
              source={initSource}
              btnRef={btnRef}
              saveSource={saveSource}
              sourceType={sourceType || []}
            />
          )}
        </div>
      </CardBody>
    </Card>
  );
}
