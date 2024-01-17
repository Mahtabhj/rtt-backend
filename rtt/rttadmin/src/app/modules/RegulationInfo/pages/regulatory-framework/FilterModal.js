import React, { useEffect, useState } from "react";
import { Button, Modal } from "react-bootstrap";
import { shallowEqual, useSelector } from "react-redux";
import ReactSelect from "react-select";

// todo delete component after rtt-514 pushed to production (pull request #)
function FilterModal({
  filterModalShow,
  handleShow,
  handleClose,
  clearFilter,
}) {
  const [filter, setFilter] = useState({});

  useEffect(() => {
    let currentFilter = JSON.parse(sessionStorage.getItem("rf_filter"));
    if (currentFilter) setFilter({ ...currentFilter });
  }, []);

  const {
    issuingBody,
    regions,
    status,
    materialCategory,
    productCategory,
  } = useSelector(
    (state) => ({
      issuingBody: state.issuingbody.entities,
      regions: state.issuingbody.regionList,
      status: state.regulatoryFramework.statusList,
      materialCategory: state.materialCategory.entities,
      productCategory: state.productCategory.entities,
    }),
    shallowEqual
  );

  let issuingBodyList = [];
  let regionList = [];
  let statusList = [];
  let materialCategoryList = [];
  let productCategoryList = [];

  issuingBody &&
    issuingBody.forEach((ib) => {
      let ibody = ib;
      issuingBodyList.push(ibody);
    });

  regions &&
    regions.forEach((r) => {
      let region = r;
      regionList.push(region);
    });

  status &&
    status.forEach((s) => {
      let st = s;
      statusList.push(st);
    });

  materialCategory &&
    materialCategory.forEach((mc) => {
      let matCat = mc;
      materialCategoryList.push(matCat);
    });

  productCategory &&
    productCategory.forEach((pc) => {
      let productCat = pc;
      productCategoryList.push(productCat);
    });

  return (
    <div>
      <Button
        variant="warning"
        onClick={() => {
          setFilter(null);
          clearFilter();
        }}
      >
        <i className="fa fa-redo"></i>
      </Button>
      <Button variant="primary ml-2" onClick={handleShow}>
        Filter
      </Button>

      <Modal show={filterModalShow} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Filter Regulatory Framework</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group mb-2 row">
            <div className=" col-lg-12 mb-2 form-group">
              <label>Issuing Body</label>
              <ReactSelect
                isMulti={false}
                value={filter && filter.issuing_body}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.name}
                onChange={(value) => {
                  setFilter({ ...filter, issuing_body: value });
                }}
                name="issuing-body"
                options={issuingBodyList}
                className="basic-multi-select"
                classNamePrefix="select"
              />
            </div>

            <div className="col-lg-12 mb-2 form-group">
              <label>Status</label>
              <ReactSelect
                isMulti={false}
                value={filter && filter.status}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.name}
                onChange={(value) => {
                  setFilter({ ...filter, status: value });
                }}
                name="status"
                options={statusList}
                className="basic-multi-select"
                classNamePrefix="select"
              />
            </div>

            <div className="col-lg-12 mb-2 form-group">
              <label>Regions</label>
              <ReactSelect
                isMulti
                value={filter && filter.regions}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.name}
                onChange={(value) => {
                  setFilter({ ...filter, regions: value });
                }}
                name="regions"
                options={regionList}
                className="basic-multi-select"
                classNamePrefix="select"
              />
            </div>

            <div className="col-lg-12 mb-2 form-group">
              <label>Material Category</label>
              <ReactSelect
                isMulti
                value={filter && filter.material_categories}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.name}
                onChange={(value) => {
                  setFilter({ ...filter, material_categories: value });
                }}
                name="material-category"
                options={materialCategoryList}
                className="basic-multi-select"
                classNamePrefix="select"
              />
            </div>

            <div className="col-lg-12 mb-2 form-group">
              <label>Product Category</label>
              <ReactSelect
                isMulti
                value={filter && filter.product_categories}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.name}
                onChange={(value) => {
                  setFilter({ ...filter, product_categories: value });
                }}
                name="product-category"
                options={productCategoryList}
                className="basic-multi-select"
                classNamePrefix="select"
              />
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => handleClose(filter)}>
            Close
          </Button>
          <Button
            variant="primary"
            onClick={() => {
              sessionStorage.setItem("rf_filter", JSON.stringify(filter));
              handleClose(filter, true);
            }}
          >
            Done
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default FilterModal;
