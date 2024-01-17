import React from "react";
import { useDispatch, useSelector } from "react-redux";
import PropTypes from "prop-types";

import { deleteFamily } from "../../../_redux/family/familyActions";
import { familyActionsLoading } from "../../../_redux/family/familySelectors";

import { DeleteModal } from "@common";

const propTypes = {
  idForDelete: PropTypes.number,
  isModalShown: PropTypes.bool.isRequired,
  closeModalCallback: PropTypes.func.isRequired,
  updateCallback: PropTypes.func.isRequired,
}

const defaultProps = {
  idForDelete: null,
}

export const FamilyDeleteModal = ({ idForDelete, isModalShown, closeModalCallback, updateCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(familyActionsLoading);

  const submitDeleteFamily = () => {
    dispatch(deleteFamily(idForDelete)).then(() => {
      updateCallback();
      closeModalCallback();
    });
  };

  return (
    <DeleteModal
      title="Are you sure you want to delete this Family?"
      isModalShown={isModalShown}
      onClose={closeModalCallback}
      onSubmit={submitDeleteFamily}
      actionsLoading={actionsLoading}
      size="md"
    />
  );
};

FamilyDeleteModal.propTypes = propTypes;
FamilyDeleteModal.defaultProps = defaultProps;
