import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Modal } from 'react-bootstrap';
import PropTypes from 'prop-types';

import { ModalProgressBar } from '@metronic-partials/controls';

import { ACTION_TYPE } from '@common';
import { addFamily } from '../../../_redux/family/familyActions';
import { familyActionsLoading } from '../../../_redux/family/familySelectors';

import { FamilyForm } from './FamilyForm';

const initialFamily = {
  chemycal_id: '',
  name: '',
};

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  closeModalCallback: PropTypes.func.isRequired,
  updateCallback: PropTypes.func.isRequired,
};

export const FamilyAddModal = ({ isModalShown, closeModalCallback, updateCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(familyActionsLoading);

  const saveFamily = ({ chemycal_id, name }) =>
    dispatch(
      addFamily({
        chemycal_id: chemycal_id.trim(),
        name: name.trim(),
      }),
    ).then(response => {
      if (!response?.type.endsWith(ACTION_TYPE.REJECTED)) {
        updateCallback();
        closeModalCallback();
      }
    });

  const handleOnHide = () => closeModalCallback();

  return (
    <Modal size="lg" show={isModalShown} onHide={handleOnHide} aria-labelledby="example-modal-sizes-title-lg">
      {actionsLoading && <ModalProgressBar variant="query" />}

      <Modal.Header>
        <Modal.Title id="example-modal-sizes-title-lg">Add Family</Modal.Title>
      </Modal.Header>

      <FamilyForm
        family={initialFamily}
        saveFamily={saveFamily}
        onCancelCallback={closeModalCallback}
        actionsLoading={actionsLoading}
      />
    </Modal>
  );
};

FamilyAddModal.propTypes = propTypes;
