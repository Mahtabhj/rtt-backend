import React, { useEffect, useMemo, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { Button, Modal } from "react-bootstrap";
import ReactSelect from "react-select";
import PropTypes from "prop-types";

import {
  updateFilter as updateNewsFilter,
  applyFilter as applyNewsFilter,
  resetFilter as resetNewsFilter
} from "@redux-news/news/newsSlice";
import {
  updateFilter as updateRegulationFilter,
  applyFilter as applyRegulationFilter,
  resetFilter as resetRegulationFilter
} from "@redux-regulation/regulation/regulationSlice";
import {
  updateFilter as updateRegulatoryFrameworkFilter,
  applyFilter as applyRegulatoryFrameworkFilter,
  resetFilter as resetRegulatoryFrameworkFilter
} from "@redux-regulation/regulatory-framework/regulatoryFrameworkSlice";
import { filterItems, reviewStatusOptions, title } from "./content";

const filterActions = {
  news: {
    updateFilter: updateNewsFilter,
    applyFilter: applyNewsFilter,
    resetFilter: resetNewsFilter
  },
  regulation: {
    updateFilter: updateRegulationFilter,
    applyFilter: applyRegulationFilter,
    resetFilter: resetRegulationFilter
  },
  regulatoryFramework: {
    updateFilter: updateRegulatoryFrameworkFilter,
    applyFilter: applyRegulatoryFrameworkFilter,
    resetFilter: resetRegulatoryFrameworkFilter
  }
};

const propTypes = {
  filterType: PropTypes.oneOf(['news', 'regulation', 'regulatoryFramework']).isRequired,
}

export function FilterModal({ filterType }) {
  const dispatch = useDispatch();

  const { filterOptions, isFiltered } = useSelector(
    (state) => ({
      filterOptions: filterType ? state[filterType].filterOptions : null,
      isFiltered: filterType ? state[filterType].isFiltered : null,
    })
  );

  useEffect(() => {
    setFilter(filterOptions)
  }, [filterOptions]);

  const [filter, setFilter] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // filterType === 'news'
  const { regionList, categoryList, newsProductCategoryList } = useSelector(
    (state) => ({
      regionList: state.news.regionList,
      categoryList: state.news.categoryList,
      newsProductCategoryList: state.news.productCategoryList,
    }),
    shallowEqual
  );

  // filterType === 'regulation'
  const { regulatoryFrameworkList, regulationTypeList } = useSelector(
    (state) => ({
      regulatoryFrameworkList: state.regulation.regulatoryFrameworkList,
      regulationTypeList: state.regulation.regulationTypeList,
    }),
    shallowEqual
  );

  const {
    issuingBodyList,
    issuingBodyRegionList,
    statusList,
    materialCategoryList,
    productCategoryList,
  } = useSelector(
    (state) => ({
      issuingBodyList: state.issuingbody.entities,
      issuingBodyRegionList: state.issuingbody.regionList,
      statusList: state.regulatoryFramework.statusList,
      materialCategoryList: state.materialCategory.entities,
      productCategoryList: state.productCategory.entities,
    }),
    shallowEqual
  );

  const options = useMemo(()=> ({
    regionList,
    categoryList,
    newsProductCategoryList,
    regulatoryFrameworkList,
    regulationTypeList,
    issuingBodyList,
    statusList,
    issuingBodyRegionList,
    materialCategoryList,
    productCategoryList,
    reviewStatusOptions,
    }
  ), [
    regionList,
    categoryList,
    newsProductCategoryList,
    regulatoryFrameworkList,
    regulationTypeList,
    issuingBodyList,
    statusList,
    issuingBodyRegionList,
    materialCategoryList,
    productCategoryList]);

  const filterModel = useMemo(() => (
    filterItems[filterType].map(item => (
      {
        ...item,
        options: options[item.options]
      }
    ))
  ), [filterType, options])

  const handleOnCLickReset = () => {
    // clear in store
    dispatch(filterActions[filterType].resetFilter());

    setFilter(null);
  };
  const handleOnClickOpen = () => {
    setIsModalOpen(true)
  };
  const handleOnClickClose = () => {
    // save in store
    !isFiltered && dispatch(filterActions[filterType].updateFilter(filter));

    setIsModalOpen(false);
  };
  const handleOnClickDone = () => {
    // save in store
    dispatch(filterActions[filterType].updateFilter(filter));
    dispatch(filterActions[filterType].applyFilter());

    setIsModalOpen(false);
  };

  const getOptionLabel = (option) => option.name;
  const getOptionValue = (option) => option.id;

  const renderFilterItem = ({ label, name, options, multi = true }) => {
    const handleOnChange = (value) => {
      setFilter({ ...filter, [name]: value });
    };
    const value = filter && filter[name];

    return (
      <div className=" col-lg-12 mb-2 form-group" key={name}>
        <label>{label}</label>
        <ReactSelect
          isMulti={multi}
          value={value}
          getOptionLabel={getOptionLabel}
          getOptionValue={getOptionValue}
          onChange={handleOnChange}
          name={name}
          options={options}
          className="basic-multi-select"
          classNamePrefix="select"
        />
      </div>
    )
  };

  return (
    <div>
      <Button variant="warning" onClick={handleOnCLickReset}>
        <i className="fa fa-redo"/>
      </Button>
      <Button variant="primary ml-2" onClick={handleOnClickOpen}>
        Filter
      </Button>

      <Modal show={isModalOpen} onHide={handleOnClickClose}>
        <Modal.Header closeButton>
          <Modal.Title>Filter {title[filterType]}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group mb-2 row">
            {filterModel.map(item => renderFilterItem(item))}
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleOnClickClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleOnClickDone}
          >
            Done
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

FilterModal.propTypes = propTypes;
