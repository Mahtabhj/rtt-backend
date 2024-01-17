import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { Card, CardBody, CardHeader, CardHeaderToolbar } from '@metronic-partials/controls';
import { ActionsDropdown, MANUAL_ADD, UPLOAD_FILE, useFiltersQuery, usePaginationQuery } from '@common';

import { setIsDroppingFilters } from '@redux/app/appActions';
import { getAllSubstanceData, getSubstanceDataFilteredIds } from '../../../_redux/substance-data/substanceDataActions';
import {
  substanceDataFilteredIdsSelector,
  substanceDataSelector,
} from '../../../_redux/substance-data/substanceDataSelectors';

import { SubstanceDataTable } from './SubstanceDataTable';
import { SubstanceDataAddEditModal } from './SubstanceDataAddEditModal';
import { SubstanceDataUploadModal } from './SubstanceDataUploadModal';
import { SubstanceDataDeleteModal } from './SubstanceDataDeleteModal';

export const SubstanceDataCard = () => {
  const dispatch = useDispatch();

  const { count, results } = useSelector(substanceDataSelector);
  const filteredIds = useSelector(substanceDataFilteredIdsSelector);

  const [ids, setIds] = useState([]);
  const [idForEdit, setIdForEdit] = useState(null);
  const [isAllSelected, setAllSelected] = useState(false);

  const [paginationQuery, setPaginationQuery, customOptions] = usePaginationQuery(count, 100);

  const dropSelectionCallback = useCallback(() => {
    setIds([]);
    setAllSelected(false);
  }, []);

  const [filtersQuery, setFiltersQuery, onTableChange] = useFiltersQuery(setPaginationQuery, dropSelectionCallback);

  const [isDeleteModalShown, setDeleteModalShown] = useState(false);
  const [isAddEditModalShown, setAddEditModalShown] = useState(false);
  const [isUploadModalShown, setUploadModalShown] = useState(false);

  const fetchSubstanceData = useCallback(() => {
    dispatch(
      getAllSubstanceData({
        limit: paginationQuery.sizePerPage,
        skip: (paginationQuery.page - 1) * paginationQuery.sizePerPage,
        ...filtersQuery,
      }),
    );
  }, [dispatch, paginationQuery, filtersQuery]);

  useEffect(() => {
    fetchSubstanceData();
  }, [fetchSubstanceData]);

  useEffect(() => {
    if (filtersQuery) {
      dispatch(getSubstanceDataFilteredIds(filtersQuery));
    }
  }, [dispatch, filtersQuery]);

  const addActionButtons = useMemo(
    () => [
      { actionName: MANUAL_ADD, actionCallback: () => setAddEditModalShown(true) },
      { actionName: UPLOAD_FILE, actionCallback: () => setUploadModalShown(true) }
    ],
    [],
  );

  const handleStartDelete = () => setDeleteModalShown(true);

  const handleStartEdit = () => {
    const [selectedSubstanceDataItemId] = ids;
    setIdForEdit(selectedSubstanceDataItemId);
    setAddEditModalShown(true);
  };

  const handleSelectAll = useCallback(() => {
    setIds(isAllSelected ? [] : filteredIds);
    setAllSelected(prevState => !prevState);
  }, [filteredIds, isAllSelected]);

  useEffect(() => {
    setAllSelected(prevState => !!ids.length && prevState);
  }, [ids]);

  const handleDropFilters = () => {
    dispatch(setIsDroppingFilters(true));
    setFiltersQuery(null);
    setIds([]);
    setTimeout(() => dispatch(setIsDroppingFilters(false)));
  };

  const handleDeleteModalClose = () => setDeleteModalShown(false);
  const handleAddEditModalClose = () => {
    setIdForEdit(null);
    setAddEditModalShown(false);
  };
  const handleUploadModalClose = () => setUploadModalShown(false);
  const handelModalUpdate = () => {
    if (idForEdit || isDeleteModalShown) {
      setIds([]);
    }

    fetchSubstanceData();
  };

  const isSelectAllButtonShown =
    isAllSelected || (!!filtersQuery && !!ids.length && ids.length >= results.length && ids.length !== count);
  const renderSelectAllButtonTitle = () => (isAllSelected ? 'Clear selection' : `Select all ${count} substances`);

  const renderActionButtons = () => !!ids.length && (
    <>
      <button
        type="button"
        className="btn btn-danger mr-5"
        onClick={handleStartDelete}
      >
        Delete
      </button>

      {ids.length === 1 && (
        <button
          type="button"
          className="btn btn-primary mr-5"
          onClick={handleStartEdit}
        >
          Edit
        </button>
      )}
    </>
  );

  const renderSelectedInfo = () => `${ids?.length} of ${isAllSelected ? count : results?.length} selected`;

  return (
    <Card>
      <CardHeader title="Substance Data">
        <CardHeaderToolbar>
          {isSelectAllButtonShown && (
            <a className="text-primary mr-5" onClick={handleSelectAll} role="button">
              {renderSelectAllButtonTitle()}
            </a>
          )}
          {renderActionButtons()}
          <span className="mr-5" style={{ minWidth: '140px', textAlign: 'right' }}>
            {renderSelectedInfo()}
          </span>
          {!!filtersQuery && (
            <button type="button" className="btn btn-primary mr-5" onClick={handleDropFilters}>
              Drop all filters
            </button>
          )}
          <ActionsDropdown title="Add Substance" buttons={addActionButtons} />
          <SubstanceDataDeleteModal
            isModalShown={isDeleteModalShown}
            idsForDelete={ids}
            closeModalCallback={handleDeleteModalClose}
            updateCallback={handelModalUpdate}
          />
          <SubstanceDataAddEditModal
            isModalShown={isAddEditModalShown}
            idForEdit={idForEdit}
            closeModalCallback={handleAddEditModalClose}
            updateCallback={handelModalUpdate}
          />
          <SubstanceDataUploadModal
            isModalShown={isUploadModalShown}
            closeModalCallback={handleUploadModalClose}
          />
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        <SubstanceDataTable
          list={results}
          customOptions={customOptions}
          checkedIds={ids}
          setCheckedIds={setIds}
          onTableChangeCallback={onTableChange}
        />
      </CardBody>
    </Card>
  );
};
