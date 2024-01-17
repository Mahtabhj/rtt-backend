import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { getProperties } from '../../_redux/substance-data/substanceDataActions';
import { substanceDataIsLoading } from '../../_redux/substance-data/substanceDataSelectors';

import { LoadingDialog } from '@metronic-partials/controls';

import { SubstanceDataCard } from './components/SubstanceDataCard';

export const SubstanceDataPage = () => {
  const dispatch = useDispatch();

  const isLoading = useSelector(substanceDataIsLoading);

  useEffect(() => {
    dispatch(getProperties());
  }, [dispatch]);

  return (
    <>
      <LoadingDialog isLoading={isLoading} text="Loading ..." />

      <SubstanceDataCard />
    </>
  );
}
