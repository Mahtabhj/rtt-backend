import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import PropTypes from "prop-types";
import dayjs from "dayjs";

import { deleteExemptions } from "../../../_redux/exemption/exemptionActions";
import { exemptionActionsLoading } from "../../../_redux/exemption/exemptionSelectors";

import { DeleteModal } from "@common";

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  idsForDelete: PropTypes.arrayOf(PropTypes.number.isRequired).isRequired,
  closeModalCallback: PropTypes.func.isRequired,
  updateCallback: PropTypes.func.isRequired,
}

export const ExemptionDeleteModal = ({ isModalShown, idsForDelete, closeModalCallback, updateCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(exemptionActionsLoading);

  const [date, setDate] = useState('');

  const submitDeleteLimits = () => {
    const dataToSend = { exemptions: idsForDelete, date: date || dayjs().toISOString() };

    dispatch(deleteExemptions(dataToSend)).then(() => {
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

ExemptionDeleteModal.propTypes = propTypes;
