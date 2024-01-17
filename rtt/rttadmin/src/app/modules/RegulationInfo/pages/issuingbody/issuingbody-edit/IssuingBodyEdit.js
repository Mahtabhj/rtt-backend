/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import React, { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { shallowEqual, useSelector } from "react-redux";

import * as actions from "@redux-regulation/issuingbody/issuingbodyActions";

import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
  ModalProgressBar,
} from "@metronic-partials/controls";
import { useSubheader } from "@metronic/layout";

import { IssuingBodyEditForm } from "./IssuingBodyEditForm";

export function IssuingBodyEdit({
  history,
  match: {
    params: { id },
  },
}) {
  const [initIssuingBody, setInitIssuingBody] = useState({
    id: undefined,
    name: "",
    region: "",
    description: "",
    urls: []
  });

  // Subheader
  const subheader = useSubheader();

  // Tabs
  const [tab] = useState("basic");
  const [title, setTitle] = useState("");
  const dispatch = useDispatch();

  const {
    actionsLoading,
    issuingbodyForEdit,
    issuingBodyRegionList,
    urlList,
  } = useSelector(
    (state) => ({
      actionsLoading: state.issuingbody.actionsLoading,
      issuingbodyForEdit: state.issuingbody.issuingbodyForEdit,
      issuingBodyRegionList: state.issuingbody.regionList,
      urlList: state.issuingbody.urlList,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.fetchIssuingBody(id));
    dispatch(actions.fetchRegionList());
    dispatch(actions.fetchURLsList());
  }, [id, dispatch]);

  useEffect(() => {
    const _title = id
      ? !!issuingbodyForEdit && `Edit Issuing Body: ${issuingbodyForEdit?.name}`
      : "Create Issuing Body";

    if (id && issuingbodyForEdit) {
      const newInit = {
        ...issuingbodyForEdit,
        region: issuingbodyForEdit.region.id,
      };
      setInitIssuingBody(newInit);
    } else if (
      !id &&
      issuingBodyRegionList &&
      issuingBodyRegionList.length > 0
    ) {
      let newInit = {
        ...initIssuingBody,
        region: issuingBodyRegionList[0].id,
      };
      setInitIssuingBody(newInit);
    }

    setTitle(_title);
    subheader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [issuingbodyForEdit, id, issuingBodyRegionList, urlList]);

  const saveIssuingBody = values => {
    if (!id) {
      dispatch(actions.createIssuingBody(values)).then(() =>
        backToIssuingBodyList()
      );
    } else {
      dispatch(actions.updateIssuingBody(values)).then(() =>
        backToIssuingBodyList()
      );
    }
  };

  const btnRef = useRef();
  const saveIssuingBodyClick = () => {
    if (btnRef && btnRef.current) {
      btnRef.current.click();
    }
  };

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
            Back
          </button>

          <button
            type="submit"
            className="btn btn-primary ml-2"
            onClick={saveIssuingBodyClick}
          >
            Save
          </button>
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <div className="mt-5">
          {tab === "basic" && (
            <IssuingBodyEditForm
              actionsLoading={actionsLoading}
              issuingbody={initIssuingBody}
              btnRef={btnRef}
              saveIssuingBody={saveIssuingBody}
              regionOptions={issuingBodyRegionList || []}
              urlList={urlList || []}
            />
          )}
        </div>
      </CardBody>
    </Card>
  );
}
