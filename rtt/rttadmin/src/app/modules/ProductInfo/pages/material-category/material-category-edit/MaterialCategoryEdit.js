/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import React, { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { shallowEqual, useSelector } from "react-redux";
import * as actions from "@redux-product/material-category/materialCategoryActions";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { MaterialCategoryEditForm } from "./MaterialCategoryEditForm";
import { useSubheader } from "@metronic/layout";
import { ModalProgressBar } from "@metronic-partials/controls";

const initMaterialCategory = {
  id: undefined,
  name: "",
  description: "",
  industry: "",
  online: true,
  image: "",
};

export function MaterialCategoryEdit({
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

  const { actionsLoading, materialCategoryForEdit, success } = useSelector(
    (state) => ({
      actionsLoading: state.materialCategory.actionsLoading,
      materialCategoryForEdit: state.materialCategory.materialCategoryForEdit,
      success: state.materialCategory.success,
    }),
    shallowEqual
  );

  useEffect(() => {
    if (success) {
      backToMaterialCategoryList()
    }
  }, [success]);

  useEffect(() => {
    dispatch(actions.fetchMaterialCategory(id));
  }, [id, dispatch]);

  useEffect(() => {
    let _title = id ? "" : "Create Material Category";
    if (materialCategoryForEdit && id) {
      _title = `Edit Material Category '${materialCategoryForEdit.name}'`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [materialCategoryForEdit, id]);

  const saveMaterialCategory = (values) => {
    if (!id) {
      dispatch(actions.createMaterialCategory(values))
    } else {
      dispatch(actions.updateMaterialCategory(values))
    }
  };

  const btnRef = useRef();
  const saveMaterialCategoryClick = () => {
    if (btnRef && btnRef.current) {
      btnRef.current.click();
    }
  };

  const backToMaterialCategoryList = () => {
    history.push(`/backend/product-info/material-categories`);
  };

  return (
    <Card>
      {actionsLoading && <ModalProgressBar />}
      <CardHeader title={title}>
        <CardHeaderToolbar>
          <button
            type="button"
            onClick={backToMaterialCategoryList}
            className="btn btn-light"
          >
            <i className="fa fa-arrow-left"></i>
            Back
          </button>
          {`  `}
          <button
            type="submit"
            className="btn btn-primary ml-2"
            onClick={saveMaterialCategoryClick}
          >
            Save
          </button>
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <div className="mt-5">
          <MaterialCategoryEditForm
            actionsLoading={actionsLoading}
            materialCategory={materialCategoryForEdit || initMaterialCategory}
            btnRef={btnRef}
            saveMaterialCategory={saveMaterialCategory}
          />
        </div>
      </CardBody>
    </Card>
  );
}
