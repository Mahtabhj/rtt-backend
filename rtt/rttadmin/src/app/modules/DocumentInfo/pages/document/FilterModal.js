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
    let currentFilter = JSON.parse(sessionStorage.getItem("dc_filter"));
    if (currentFilter) setFilter({ ...currentFilter });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const { typeList, regulations } = useSelector(
    (state) => ({
      typeList: state.document.documentTypeList,
      regulations: state.regulation.entities,
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
          <Modal.Title>Filter Regulatory Framework</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group mb-2 row">
            <div className=" col-lg-12 mb-2 form-group">
              <label>Document Type</label>
              <ReactSelect
                isMulti={false}
                value={filter && filter.types}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.id}
                onChange={(value) => {
                  setFilter({ ...filter, types: value });
                }}
                name="issuing-body"
                options={typeList}
                className="basic-multi-select"
                classNamePrefix="select"
              />
            </div>
            <div className=" col-lg-12 mb-2 form-group">
              <label>Regulations</label>
              <ReactSelect
                isMulti={true}
                value={filter && filter.regulations}
                getOptionLabel={(option) => option.name}
                getOptionValue={(option) => option.id}
                onChange={(value) => {
                  setFilter({ ...filter, regulations: value });
                }}
                name="issuing-body"
                options={regulations}
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
              sessionStorage.setItem("dc_filter", JSON.stringify(filter));
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
