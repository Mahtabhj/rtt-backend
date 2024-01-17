import React, { useCallback, useEffect, useMemo, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import PropTypes from "prop-types";

import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";

import { fetchRelatedSubstances, addOrRemoveSubstancesManually } from "@redux/substances/substancesActions";

import { ActionsDropdown } from "../ActionsDropdown/ActionsDropdown";
import { AddSubstanceModal } from "./components/AddSubstanceModal";
import { ConfirmationModal } from "../ConfirmationModal/ConfirmationModal";
import { Search } from "../Search/Search";
import { SubstancesTable } from "../SubstancesTable/SubstancesTable";

const propTypes = {
  queryParams: PropTypes.object,
  isCard: PropTypes.bool.isRequired,
}

const defaultProps = {
  queryParams: null
}

export const RelatedSubstances = ({ queryParams, isCard }) => {
  const dispatch = useDispatch();

  const [substances, setSubstances] = useState([]);
  const [ids, setIds] = useState([]);
  const [isAllSelected, setAllSelected] = useState(false);
  const [state, setState] = useState({
    page: 1,
    sizePerPage: 10,
    search: '',
  });
  const [isDeleteConfirmationModalShown, setDeleteConfirmationModalShown] = useState(false);
  const [isDeleting, setDeleting] = useState(false);

  const {
    relatedSubstances: { count, results },
  } = useSelector(
    (state) => ({
      relatedSubstances: state.substances.relatedSubstances,
    }),
  );

  const totalCount = useMemo(() => (count || substances.length), [count, substances.length]);

  const fetchSubstances = useCallback(() => {
    if (queryParams) {
      dispatch(fetchRelatedSubstances({
        ...queryParams,
        limit: state.sizePerPage,
        skip: (state.page - 1) * state.sizePerPage,
        search: state.search,
      }));
    }
  }, [dispatch, queryParams, state]);

  useEffect(() => {
    fetchSubstances();
  }, [fetchSubstances]);

  useEffect(() => {
    setSubstances(results);
  } ,[results]);

  useEffect(() => {
    if (isAllSelected) setIds(substances.map(({ id }) => id));
  }, [isAllSelected, substances]);

  useEffect(() => {
    if (isAllSelected && substances.length !== ids.length) setAllSelected(false);
  }, [isAllSelected, substances, ids]);

  const customOptions = useMemo(() => ({
    totalSize: totalCount,
    sizePerPage: state.sizePerPage,
    sizePerPageList: [
      { text: "10", value: 10 },
      { text: "50", value: 50 },
      { text: "100", value: 100 },
    ],
    hideSizePerPage: false,
  }), [totalCount, state.sizePerPage]);

  const handleOnSearchInputChange = useCallback(value => {
    setState(prevState => ({ page: prevState.page, sizePerPage: prevState.sizePerPage, search: value }));
    setIds([]);
  }, []);

  const onTableChange = useCallback((type, { page, sizePerPage }) => {
    if (type === 'pagination') {
      setIds([]);
      setState(prevState => ({ page, sizePerPage, search: prevState.search }));
    }
  }, []);

  const handleSelectAll = useCallback(() => {
    setIds(isAllSelected ? [] : substances.map(({ id }) => id));
    setAllSelected(prevState => !prevState);
  },[substances, isAllSelected]);

  const handleOnRemove = useCallback(() => {
    setDeleting(true);
    const dataToSend = isAllSelected ? {
      substances: [],
      action: 'remove-all',
    } : {
      substances: ids,
      action: 'remove',
    };

    dispatch(addOrRemoveSubstancesManually(dataToSend)).then(() => {
      setIds([]);
      setDeleting(false);
      setDeleteConfirmationModalShown(false);
      fetchSubstances();
    });
  }, [dispatch, fetchSubstances, isAllSelected, ids]);

  const actionsDropdownButtons = useMemo(() => (
    [{ actionName: 'Remove', actionCallback: () => setDeleteConfirmationModalShown(true), isDanger: true }]
  ), []);

  const handleOnHideConfirmationModal = () => setDeleteConfirmationModalShown(false);

  const renderSelectAllButtonTitle = () => !state.search && (
    isAllSelected || ids.length === totalCount
      ? 'Clear selection'
      : `Select${totalCount > 1 ? ' all' : ''} ${totalCount} substance${totalCount > 1 ? 's' : ''}`
  );

  const renderSelectedInfo = () =>
    `${isAllSelected ? totalCount : ids.length} of ${isAllSelected ? totalCount : substances.length} selected`;

  const renderHeaderToolbar = () => (
    <>
      {!!substances.length && (
        <>
          {ids.length === substances.length && (
            <a
              className="text-primary mr-5"
              onClick={handleSelectAll}
              role="button"
            >
              {renderSelectAllButtonTitle()}
            </a>
          )}
          {!!ids.length && <ActionsDropdown title="Actions" buttons={actionsDropdownButtons}/>}
          <ConfirmationModal
            isShown={isDeleteConfirmationModalShown}
            isLoading={isDeleting}
            onSubmitCallback={handleOnRemove}
            onHideCallback={handleOnHideConfirmationModal}
          />
          <span className="mr-5 ml-5" style={{ minWidth: '120px', textAlign: 'right' }}>{renderSelectedInfo()}</span>
        </>
      )}
      <AddSubstanceModal updateCallback={fetchSubstances} />
    </>
  );

  const renderSubstanceTable = () => (
    <SubstancesTable
      substances={substances}
      customOptions={customOptions}
      checkedIds={ids}
      setCheckedIds={setIds}
      onTableChangeCallback={onTableChange}
    />
  );

  if (!queryParams) return (<></>);

  return (
    <>
      <div className="mb-5" style={{ maxWidth: '320px' }}>
        <Search
          initialValue={state.search}
          handleUpdateSearch={handleOnSearchInputChange}
          placeholder='Search by Name, EC, CAS'
        />
      </div>
      {isCard ? (
        <Card>
          <CardHeader title="Related Substances">
            <CardHeaderToolbar>
              {renderHeaderToolbar()}
            </CardHeaderToolbar>
          </CardHeader>

          {renderSubstanceTable()}
        </Card>
      ) : (
        <>
          <div className="d-flex justify-content-between align-items-center">
            <label>Select Substances</label>

            <div className="d-flex align-items-center">
              {renderHeaderToolbar()}
            </div>
          </div>

          {renderSubstanceTable()}
        </>
      )}
    </>
  )
}

RelatedSubstances.propTypes = propTypes;
RelatedSubstances.defaultProps = defaultProps;
