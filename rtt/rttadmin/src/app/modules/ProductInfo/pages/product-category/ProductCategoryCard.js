import React, { useMemo, useState, useEffect } from "react";

import { useDispatch } from "react-redux";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import FilterModal from "./FilterModal";
import { ProductCategoryTable } from "./product-category-table/ProductCategoryTable";
import * as actions from "@redux-product/product-category/productCategoryActions";
import { useProductCategoryUIContext } from "./ProductCategoryUIContext";

export function ProductCategoryCard() {
  const productCategoryUIContext = useProductCategoryUIContext();
  const [filterModalShow, setFilterModalShow] = useState(false);
  const [filter, setFilter] = useState(null);
  const [searchValue, setSearchvalue] = useState("");

  const [industry, setIndustry] = useState([]);
  const productCategoryUIProps = useMemo(() => {
    return {
      ids: productCategoryUIContext.ids,
      queryParams: productCategoryUIContext.queryParams,
      setQueryParams: productCategoryUIContext.setQueryParams,
      newProductCategoryButtonClick:
        productCategoryUIContext.newProductCategoryButtonClick,
      openDeleteProductCategoryDialog:
        productCategoryUIContext.openDeleteProductCategoryDialog,
      openEditProductCategoryPage:
        productCategoryUIContext.openEditProductCategoryPage,
      openUpdateProductCategoryStatusDialog:
        productCategoryUIContext.openUpdateProductCategoryStatusDialog,
      openFetchProductCategoryDialog:
        productCategoryUIContext.openFetchProductCategoryDialog,
    };
  }, [productCategoryUIContext]);

  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(actions.fetchIndustryList());
  }, [dispatch]);

  useEffect(() => {
    dispatch(
      actions.fetchProductCategoryList({
        search: searchValue,
        industry: industry,
      })
    );

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchValue, dispatch, industry]);

  const handleClose = (filter, clicked = false) => {
    if (clicked) {
      const industry =
        filter.industry && filter.industry.map((value) => value.id);
      setIndustry(industry && industry.join(","));
      setFilterModalShow(false);
    } else {
      setFilterModalShow(false);
    }
  };
  const handleShow = () => setFilterModalShow(true);
  const emptyFilter = () => {
    setIndustry(null);
    setFilter(null);
    setSearchvalue(null);
    document.getElementById("search").value = "";
    sessionStorage.removeItem("pc_filter");
  };

  return (
    <Card>
      <CardHeader title="Product Category List">
        <CardHeaderToolbar>
          <button
            type="button"
            className="btn btn-primary"
            onClick={productCategoryUIProps.newProductCategoryButtonClick}
          >
            Create Product Category{" "}
          </button>
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        <div className="d-flex justify-content-between flex-wrap">
          <div className="form-group">
            <input
              id="search"
              type="text"
              className="form-control"
              placeholder="Search..."
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  let value = e.target.value;
                  setSearchvalue(value);
                }
              }}
            />
          </div>
          <div className="popup">
            <FilterModal
              filterModalShow={filterModalShow}
              handleShow={handleShow}
              handleClose={handleClose}
              clearFilter={emptyFilter}
              setFilter={setFilter}
              filter={filter}
            />
          </div>
        </div>
        {productCategoryUIProps.ids.length > 0}
        <ProductCategoryTable filter={industry} search={searchValue} />
      </CardBody>
    </Card>
  );
}
