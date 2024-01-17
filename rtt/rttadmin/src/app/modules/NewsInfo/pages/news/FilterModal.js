import React, { useEffect } from "react";
import { Button, Modal } from "react-bootstrap";
import { shallowEqual, useSelector } from "react-redux";
import ReactSelect from "react-select";

// todo delete component after rtt-512 pushed to production (pull request #73)
function FilterModal({
  filterModalShow,
  handleShow,
  handleClose,
  clearFilter,
  setFilter,
  filter,
}) {
  useEffect(() => {
    let currentFilter = JSON.parse(sessionStorage.getItem("nc_filter"));
    if (currentFilter) setFilter({ ...currentFilter });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const { regionList, categoryList, productCategoryList } = useSelector(
    (state) => ({
      regionList: state.news.regionList,
      categoryList: state.news.categoryList,
      productCategoryList: state.news.productCategoryList,
    }),
    shallowEqual
  );
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
          <Modal.Title>Filter News</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group mb-2 row">
            <div className=" col-lg-12 mb-2 form-group">
              <label>Regions</label>
              <ReactSelect
                isMulti={true}
                value={filter && filter.regions}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.id}
                onChange={(value) => {
                  setFilter({ ...filter, regions: value });
                }}
                name="regions"
                options={regionList}
                className="basic-multi-select"
                classNamePrefix="select"
              />
            </div>
            <div className=" col-lg-12 mb-2 form-group">
              <label>News Category</label>
              <ReactSelect
                isMulti={true}
                value={filter && filter.news_category}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.id}
                onChange={(value) => {
                  setFilter({ ...filter, news_category: value });
                }}
                name="new_category"
                options={categoryList}
                className="basic-multi-select"
                classNamePrefix="select"
              />
            </div>
            <div className=" col-lg-12 mb-2 form-group">
              <label>Product Category</label>
              <ReactSelect
                isMulti={true}
                value={filter && filter.product_category}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.id}
                onChange={(value) => {
                  setFilter({ ...filter, product_category: value });
                }}
                name="new_category"
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
              sessionStorage.setItem("nc_filter", JSON.stringify(filter));
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
