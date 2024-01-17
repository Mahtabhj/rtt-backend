import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import PropTypes from "prop-types";
import dayjs from "dayjs";

import { deleteLimits } from "../../../_redux/limit/limitActions";
import { limitActionsLoading } from "../../../_redux/limit/limitSelectors";

import { DeleteModal } from "@common";

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  idsForDelete: PropTypes.arrayOf(PropTypes.number.isRequired).isRequired,
  closeModalCallback: PropTypes.func.isRequired,
  updateCallback: PropTypes.func.isRequired,
}

export const LimitDeleteModal = ({ isModalShown, idsForDelete, closeModalCallback, updateCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(limitActionsLoading);

  const [date, setDate] = useState('');

  const submitDeleteLimits = () => {
    const dataToSend = { limits: idsForDelete, date: date || dayjs().toISOString() };

    dispatch(deleteLimits(dataToSend)).then(() => {
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
      onSubmit={submitDeleteLimits}
      actionsLoading={actionsLoading}
    />
  );
}

LimitDeleteModal.propTypes = propTypes;
