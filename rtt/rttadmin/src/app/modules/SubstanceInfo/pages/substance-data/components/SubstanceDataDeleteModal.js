import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';
import dayjs from 'dayjs';

import { deleteSubstanceData } from '../../../_redux/substance-data/substanceDataActions';
import { substanceDataActionsLoading } from '../../../_redux/substance-data/substanceDataSelectors';

import { DeleteModal } from '@common';

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  idsForDelete: PropTypes.arrayOf(PropTypes.number.isRequired).isRequired,
  closeModalCallback: PropTypes.func.isRequired,
  updateCallback: PropTypes.func.isRequired,
}

export const SubstanceDataDeleteModal = ({ isModalShown, idsForDelete, closeModalCallback, updateCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(substanceDataActionsLoading);

  const [date, setDate] = useState('');

  const submitDeleteSubstanceData = () => {
    const dataToSend = { substance_data: idsForDelete, date: date || dayjs().toISOString() };

    dispatch(deleteSubstanceData(dataToSend)).then(() => {
      updateCallback();
      closeModalCallback();
    });
  };

  return (
    <DeleteModal
      isModalShown={isModalShown}
      itemsCount={idsForDelete.length}
      date={date}
      setDate={setDate}
      onClose={closeModalCallback}
      onSubmit={submitDeleteSubstanceData}
      actionsLoading={actionsLoading}
    />
  );
}

SubstanceDataDeleteModal.propTypes = propTypes;
