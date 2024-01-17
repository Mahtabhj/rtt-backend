import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import dayjs from 'dayjs';

import { setIsDroppingFilters } from '@redux/app/appActions';
import { getAllLimits, getLimitFilteredIds } from '../../../_redux/limit/limitActions';
import { limitFilteredIdsSelector, limitSelector } from '../../../_redux/limit/limitSelectors';

import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from '@metronic-partials/controls';
import { DATE_FORMAT_FOR_REQUEST, MANUAL_ADD, UPLOAD_FILE } from '@common';

import { ActionsDropdown } from '@common/ActionsDropdown/ActionsDropdown';

import { LimitTable } from './LimitTable';
import { LimitAddEditModal } from './LimitAddEditModal';
import { LimitUploadModal } from './LimitUploadModal';
import { LimitDeleteModal } from './LimitDeleteModal';

export const LimitCard = () => {
  const dispatch = useDispatch();

  const { count, results } = useSelector(limitSelector);
  const filteredIds = useSelector(limitFilteredIdsSelector);

  const [ids, setIds] = useState([]);
  const [idsForEdit, setIdsForEdit] = useState([]);
  const [isAllSelected, setAllSelected] = useState(false);

  const [paginationQuery, setPaginationQuery] = useState({
    page: 1,
    sizePerPage: 20,
  });

  const [filtersQuery, setFiltersQuery] = useState(null);

  const [isDeleteModalShown, setDeleteModalShown] = useState(false);
  const [isAddEditModalShown, setAddEditModalShown] = useState(false);
  const [isUploadModalShown, setUploadModalShown] = useState(false);

  const fetchLimits = useCallback(() => {
    dispatch(getAllLimits({
      limit: paginationQuery.sizePerPage,
      skip: (paginationQuery.page - 1) * paginationQuery.sizePerPage,
      ...filtersQuery,
    }));
  }, [dispatch, paginationQuery, filtersQuery]);

  useEffect(() => {
    fetchLimits();
  }, [fetchLimits]);

  useEffect(() => {
    if (filtersQuery) {
      dispatch(getLimitFilteredIds(filtersQuery));
    }
  }, [dispatch, filtersQuery]);

  const customOptions = useMemo(() => ({
    totalSize: count,
    page: paginationQuery.page,
    sizePerPage: paginationQuery.sizePerPage,
    sizePerPageList: [
      { text: "20", value: 20 },
      { text: "50", value: 50 },
      { text: "100", value: 100 },
    ],
    hideSizePerPage: false,
  }), [count, paginationQuery]);

  const onTableChange = useCallback((type, { page, sizePerPage, filters }) => {
    const dropSelection = () => {
      setIds([]);
      setAllSelected(false);
    }

    if (type === 'pagination') {
      setPaginationQuery(prevState => ({ page: prevState.sizePerPage === sizePerPage ? page : 1, sizePerPage }));
      // dropSelection();
    }
    if (type === 'filter') {
      const filterKeys = Object.keys(filters);
      const newFiltersEntries = filterKeys.map(key => [key, filters[key].filterVal]);
      const newFilters = Object.fromEntries(newFiltersEntries);

      if (newFilters.regions) {
        newFilters.region = newFilters.regions;
        delete newFilters.regions;
      }

      if (newFilters.scope) {
        newFilters.search = newFilters.scope;
        delete newFilters.scope;
      }

      const { limit_value: limitFilters, date_into_force: dateFilters } = newFilters;

      if (limitFilters) {
        delete newFilters.limit_value;
        setFiltersQuery({ ...newFilters, min_limit_value: limitFilters.min, max_limit_value: limitFilters.max })
      } else if (dateFilters) {
        delete newFilters.date_into_force;
        setFiltersQuery({
            ...newFilters,
          from_date: dayjs(dateFilters.from).format(DATE_FORMAT_FOR_REQUEST),
          to_date: dayjs(dateFilters.to).format(DATE_FORMAT_FOR_REQUEST),
        })
      } else {
        setFiltersQuery(filterKeys.length ? newFilters : null);
      }

      dropSelection();
    }
  }, []);

  const addActionButtons = useMemo(() => (
    [
      { actionName: MANUAL_ADD, actionCallback: () => setAddEditModalShown(true) },
      { actionName: UPLOAD_FILE, actionCallback: () => setUploadModalShown(true) }
    ]
  ), []);

  const handleStartDelete = () => setDeleteModalShown(true);

  const handleStartEdit = () => {
    setIdsForEdit(ids);
    setAddEditModalShown(true);
  };

  const handleSelectAll = useCallback(() => {
    setIds(isAllSelected ? [] : filteredIds)
    setAllSelected(prevState => !prevState);
  },[filteredIds, isAllSelected]);

  useEffect(() => {
    setAllSelected(prevState => !!ids.length && prevState)
  }, [ids]);

  const handleDropFilters = () => {
    dispatch(setIsDroppingFilters(true));
    setFiltersQuery(null);
    setIds([]);
    setTimeout(() => dispatch(setIsDroppingFilters(false)));
  };

  const handleDeleteModalClose = () => setDeleteModalShown(false);
  const handleAddEditModalClose = () => {
    setIdsForEdit([]);
    setAddEditModalShown(false);
  };
  const handleUploadModalClose = () => setUploadModalShown(false);
  const handelModalUpdate = () => {
    if (idsForEdit.length || isDeleteModalShown) {
      setIds([]);
    }

    fetchLimits();
  };

  const isSelectAllButtonShown =
    isAllSelected
    || (!!filtersQuery && !!ids.length && ids.length >= results.length && ids.length !== count);
  const renderSelectAllButtonTitle = () => isAllSelected ? 'Clear selection' : `Select all ${count} limits`;

  const renderActionButtons = () => !!ids.length && (
    <>
      <button
        type="button"
        className="btn btn-danger mr-5"
        onClick={handleStartDelete}
      >
        Delete
      </button>

      <button
        type="button"
        className="btn btn-primary mr-5"
        onClick={handleStartEdit}
      >
        {ids.length === 1 ? 'Edit' : 'Bulk edit'}
      </button>
    </>
  );

  const renderSelectedInfo = () => `${ids?.length} of ${isAllSelected ? count : results?.length} selected`;

  return (
    <Card>
      <CardHeader title="Limits List">
        <CardHeaderToolbar>
          {isSelectAllButtonShown && (
            <a
              className="text-primary mr-5"
              onClick={handleSelectAll}
              role="button"
            >
              {renderSelectAllButtonTitle()}
            </a>
          )}
          {renderActionButtons()}
          <span className="mr-5" style={{ minWidth: '140px', textAlign: 'right' }}>{renderSelectedInfo()}</span>
          {!!filtersQuery && (
            <button
              type="button"
              className="btn btn-primary mr-5"
              onClick={handleDropFilters}
            >
              Drop all filters
            </button>
          )}
          <ActionsDropdown title="Add Limit" buttons={addActionButtons} />
          <LimitDeleteModal
            isModalShown={isDeleteModalShown}
            idsForDelete={ids}
            closeModalCallback={handleDeleteModalClose}
            updateCallback={handelModalUpdate}
          />
          <LimitAddEditModal
            isModalShown={isAddEditModalShown}
            idsForEdit={idsForEdit}
            closeModalCallback={handleAddEditModalClose}
            updateCallback={handelModalUpdate}
          />
          <LimitUploadModal
            isModalShown={isUploadModalShown}
            closeModalCallback={handleUploadModalClose}
          />
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        <LimitTable
          list={results}
          customOptions={customOptions}
          checkedIds={ids}
          setCheckedIds={setIds}
          onTableChangeCallback={onTableChange}
        />
      </CardBody>
    </Card>
  );
}
