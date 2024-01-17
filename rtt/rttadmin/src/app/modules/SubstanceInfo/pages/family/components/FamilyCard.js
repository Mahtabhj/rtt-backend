import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { Card, CardBody, CardHeader, CardHeaderToolbar } from '@metronic-partials/controls';

import { setIsDroppingFilters } from '@redux/app/appActions';
import { getAllFamilies } from '../../../_redux/family/familyActions';
import { familySelector } from '../../../_redux/family/familySelectors';

import { FamilyTable } from './FamilyTable';
import { FamilyAddModal } from './FamilyAddModal';
import { FamilyDeleteModal } from './FamilyDeleteModal'

export const FamilyCard = () => {
  const dispatch = useDispatch();

  const { count, results } = useSelector(familySelector);

  const [paginationQuery, setPaginationQuery] = useState({
    page: 1,
    sizePerPage: 20,
  });

  const [filtersQuery, setFiltersQuery] = useState(null);

  const [isAddModalShown, setAddModalShown] = useState(false);

  const [idForDelete, setIdForDelete] = useState(null);

  const fetchFamilies = useCallback(() => {
    dispatch(
      getAllFamilies({
        limit: paginationQuery.sizePerPage,
        skip: (paginationQuery.page - 1) * paginationQuery.sizePerPage,
        ...filtersQuery,
      }),
    );
  }, [dispatch, paginationQuery, filtersQuery]);

  useEffect(() => {
    fetchFamilies();
  }, [fetchFamilies]);

  const customOptions = useMemo(
    () => ({
      totalSize: count,
      page: paginationQuery.page,
      sizePerPage: paginationQuery.sizePerPage,
      sizePerPageList: [
        { text: '20', value: 20 },
        { text: '50', value: 50 },
        { text: '100', value: 100 },
      ],
      hideSizePerPage: false,
    }),
    [count, paginationQuery],
  );

  const onTableChange = useCallback((type, { page, sizePerPage, filters }) => {
    if (type === 'pagination') {
      setPaginationQuery(prevState => ({ page: prevState.sizePerPage === sizePerPage ? page : 1, sizePerPage }));
    }
    if (type === 'filter') {
      const filterKeys = Object.keys(filters);
      const newFiltersEntries = filterKeys.map(key => [key, filters[key].filterVal]);
      const newFilters = Object.fromEntries(newFiltersEntries);

      setFiltersQuery(filterKeys.length ? newFilters : null);
    }
  }, []);

  const handleStartAdd = () => setAddModalShown(true);
  const handleStartDelete = useCallback(familyId => {
    setIdForDelete(familyId);
  }, []);

  const handleDropFilters = () => {
    dispatch(setIsDroppingFilters(true));
    setFiltersQuery(null);
    setTimeout(() => dispatch(setIsDroppingFilters(false)));
  };

  const handleAddModalClose = useCallback(() => setAddModalShown(false), []);
  const handleDeleteModalClose = useCallback(() => setIdForDelete(null), [])

  return (
    <Card>
      <CardHeader title="Substance Families">
        <CardHeaderToolbar>
          {!!filtersQuery && (
            <button type="button" className="btn btn-primary mr-5" onClick={handleDropFilters}>
              Drop all filters
            </button>
          )}
          <button type="button" className="btn btn-primary mr-5" onClick={handleStartAdd}>
            Add Family
          </button>
          <FamilyAddModal
            isModalShown={isAddModalShown}
            closeModalCallback={handleAddModalClose}
            updateCallback={fetchFamilies}
          />
          <FamilyDeleteModal
            idForDelete={idForDelete}
            isModalShown={!!idForDelete}
            closeModalCallback={handleDeleteModalClose}
            updateCallback={fetchFamilies}
          />
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        <FamilyTable
          list={results}
          customOptions={customOptions}
          openDeleteFamilyDialog={handleStartDelete}
          onTableChangeCallback={onTableChange}
        />
      </CardBody>
    </Card>
  );
};
