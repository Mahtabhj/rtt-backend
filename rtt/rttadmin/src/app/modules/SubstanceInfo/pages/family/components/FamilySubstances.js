import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';

import { ActionsDropdown, MANUAL_ADD, UPLOAD_FILE, useFiltersQuery, usePaginationQuery } from '@common';
import { UiKitProgressBar } from '@common/UIKit';

import { setIsDroppingFilters } from '@redux/app/appActions';
import { getFamilySubstances, getFamilySubstancesFilteredIds } from '../../../_redux/family/familyActions';
import {
  familyIsLoading,
  familySubstancesFilteredIdsSelector,
  familySubstancesSelector
} from '../../../_redux/family/familySelectors';

import { FamilySubstancesTable } from './FamilySubstancesTable';
import { FamilySubstancesAddModal } from './FamilySubstancesAddModal';
import { FamilySubstancesUploadModal } from "./FamilySubstancesUploadModal";
import { FamilySubstancesDeleteModal } from './FamilySubstancesDeleteModal'

const propTypes = {
  family: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
  }).isRequired,
};

export const FamilySubstances = ({ family }) => {
  const dispatch = useDispatch();

  const { count, results } = useSelector(familySubstancesSelector);
  const filteredIds = useSelector(familySubstancesFilteredIdsSelector);
  const isLoading = useSelector(familyIsLoading);

  const [ids, setIds] = useState([]);
  const [isAllSelected, setAllSelected] = useState(false);

  const [paginationQuery, setPaginationQuery, customOptions] = usePaginationQuery(count, 100);

  const dropSelectionCallback = useCallback(() => {
    setIds([]);
    setAllSelected(false);
  }, []);

  const [filtersQuery, setFiltersQuery, onTableChange] = useFiltersQuery(setPaginationQuery, dropSelectionCallback);

  const [isDeleteModalShown, setDeleteModalShown] = useState(false);
  const [isAddModalShown, setAddEditModalShown] = useState(false);
  const [isUploadModalShown, setUploadModalShown] = useState(false);

  const fetchFamilySubstances = useCallback(() => {
    dispatch(
      getFamilySubstances({
        id: family.id,
        limit: paginationQuery.sizePerPage,
        skip: (paginationQuery.page - 1) * paginationQuery.sizePerPage,
        ...filtersQuery,
      }),
    );
  }, [dispatch, paginationQuery, filtersQuery]);

  useEffect(() => {
    fetchFamilySubstances();
  }, [fetchFamilySubstances]);

  useEffect(() => {
    if (filtersQuery) {
      dispatch(
        getFamilySubstancesFilteredIds({
          id: family.id,
          ...filtersQuery,
        })
      );
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
  const handleAddEditModalClose = () => setAddEditModalShown(false);
  const handleUploadModalClose = () => setUploadModalShown(false);
  const handelModalUpdate = () => {
    if (isDeleteModalShown) {
      setIds([]);
    }

    fetchFamilySubstances();
  };

  const isSelectAllButtonShown =
    isAllSelected || (!!filtersQuery && !!ids.length && ids.length >= results.length && ids.length !== count);
  const renderSelectAllButtonTitle = () => (isAllSelected ? 'Clear selection' : `Select all ${count} substances`);

  const renderSelectedInfo = () => `${ids?.length} of ${isAllSelected ? count : results?.length} selected`;

  return (
    <div>
      <div className="d-flex align-items-center justify-content-end mb-3">
        {isSelectAllButtonShown && (
          <a className="text-primary mr-5" onClick={handleSelectAll} role="button">
            {renderSelectAllButtonTitle()}
          </a>
        )}
        {!!ids.length && (
          <button
            type="button"
            className="btn btn-danger mr-5"
            onClick={handleStartDelete}
          >
            Remove
          </button>
        )}
        <span className="mr-5" style={{ minWidth: '140px', textAlign: 'right' }}>
          {renderSelectedInfo()}
        </span>
        {!!filtersQuery && (
          <button type="button" className="btn btn-primary mr-5" onClick={handleDropFilters}>
            Drop all filters
          </button>
        )}
        <ActionsDropdown title="Add Substance" buttons={addActionButtons} />
        <FamilySubstancesAddModal
          family={family}
          isModalShown={isAddModalShown}
          closeModalCallback={handleAddEditModalClose}
          updateCallback={handelModalUpdate}
        />
        <FamilySubstancesUploadModal
          family={family}
          isModalShown={isUploadModalShown}
          closeModalCallback={handleUploadModalClose}
        />
        <FamilySubstancesDeleteModal
            familyId={family.id}
            idsForDelete={ids}
            isModalShown={isDeleteModalShown}
            closeModalCallback={handleDeleteModalClose}
            updateCallback={handelModalUpdate}
        />
      </div>

      <UiKitProgressBar isLoading={isLoading} variant="query" />

      <FamilySubstancesTable
        list={results}
        customOptions={customOptions}
        checkedIds={ids}
        setCheckedIds={setIds}
        onTableChangeCallback={onTableChange}
      />
    </div>
  );
};

FamilySubstances.propTypes = propTypes;
