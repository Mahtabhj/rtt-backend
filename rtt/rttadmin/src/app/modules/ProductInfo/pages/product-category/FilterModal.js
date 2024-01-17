import React, { useEffect } from "react";
import { Button, Modal } from "react-bootstrap";
import { shallowEqual, useSelector } from "react-redux";
import ReactSelect from "react-select";

function FilterModal({
  filterModalShow,
  handleShow,
  handleClose,
  clearFilter,
  setFilter,
  filter,
}) {
  useEffect(() => {
    let currentFilter = JSON.parse(sessionStorage.getItem("pc_filter"));
    if (currentFilter) setFilter({ ...currentFilter });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const { industryList } = useSelector(
    (state) => ({
      industryList: state.productCategory.industryList,
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
          <Modal.Title>Filter Product Category</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group mb-2 row">
            <div className=" col-lg-12 mb-2 form-group">
              <label>Industry</label>
              <ReactSelect
                isMulti={true}
                value={filter && filter.industryList}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.id}
                onChange={(value) => {
                  setFilter({ ...filter, industry: value });
                }}
                name="industry"
                options={industryList}
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
              sessionStorage.setItem("pc_filter", JSON.stringify(filter));
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
