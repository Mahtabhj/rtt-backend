import React, { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { shallowEqual, useSelector } from "react-redux";
import * as actions from "@redux-product/product-category/productCategoryActions";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import { ProductCategoryEditForm } from "./ProductCategoryEditForm";
import { useSubheader } from "@metronic/layout";
import { ModalProgressBar } from "@metronic-partials/controls";

export function ProductCategoryEdit({
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

  const { actionsLoading, productCategoryForEdit, industryList } = useSelector(
    (state) => ({
      actionsLoading: state.productCategory.actionsLoading,
      productCategoryForEdit: state.productCategory.productCategoryForEdit,
      industryList: state.productCategory.industryList,
    }),
    shallowEqual
  );

  const [initProductCategory, setInitProductCategory] = useState({
    id: undefined,
    name: "",
    description: "",
    online: true,
    parent: "",
    industry: [],
    image: "",
  });

  useEffect(() => {
    dispatch(actions.fetchProductCategory(id));
    dispatch(actions.fetchIndustryList(id));
  }, [id, dispatch]);

  useEffect(() => {
    if (id && productCategoryForEdit && industryList) {
      let newProductCategoryForEdit = {
        ...productCategoryForEdit,
        industry: industryList.filter(({ id }) => {
          return productCategoryForEdit.industry.includes(id);
        }),
      };
      setInitProductCategory(newProductCategoryForEdit);
    } else {
      setInitProductCategory((initProductCategory) => ({
        ...initProductCategory,
      }));
    }
  }, [id, industryList, productCategoryForEdit]);

  useEffect(() => {
    let _title = id ? "" : "Create Product Category";
    if (productCategoryForEdit && id) {
      _title = `Edit Product Category '${productCategoryForEdit.name}'`;
    }

    setTitle(_title);
    suhbeader.setTitle(_title);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [productCategoryForEdit, id]);

  const saveProductCategory = (values) => {
    if (!id) {
      dispatch(actions.createProductCategory(values)).then(() =>
        backToProductCategoryList()
      );
    } else {
      dispatch(actions.updateProductCategory(values)).then(() =>
        backToProductCategoryList()
      );
    }
  };

  const btnRef = useRef();
  const saveProductCategoryClick = () => {
    if (btnRef && btnRef.current) {
      btnRef.current.click();
    }
  };

  const backToProductCategoryList = () => {
    history.push(`/backend/product-info/product-categories`);
  };

  return (
    <Card>
      {actionsLoading && <ModalProgressBar />}
      <CardHeader title={title}>
        <CardHeaderToolbar>
          <button
            type="button"
            onClick={backToProductCategoryList}
            className="btn btn-light"
          >
            <i className="fa fa-arrow-left"></i>
            Back
          </button>
          {`  `}
          <button
            type="submit"
            className="btn btn-primary ml-2"
            onClick={saveProductCategoryClick}
          >
            Save
          </button>
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <div className="mt-5">
          <ProductCategoryEditForm
            actionsLoading={actionsLoading}
            productCategory={initProductCategory}
            btnRef={btnRef}
            saveProductCategory={saveProductCategory}
            industryList={industryList || []}
          />
        </div>
      </CardBody>
    </Card>
  );
}
