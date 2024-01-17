import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Modal } from "react-bootstrap";
import PropTypes from "prop-types";
import dayjs from "dayjs";

import { addExemption, editExemption, getExemptionForEdit } from "../../../_redux/exemption/exemptionActions";
import { exemptionActionsLoading } from "../../../_redux/exemption/exemptionSelectors";

import { ModalProgressBar } from "@metronic-partials/controls";

import { ExemptionForm } from "./ExemptionForm";

const initialExemption = {
  regulation: '',
  regulatory_framework: '',
  substance: null,
  article: '',
  reference: '',
  application: '',
  expiration_date: '',
  date_into_force: '',
  status: 'active',
  modified: dayjs().toISOString(),
};

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  idForEdit: PropTypes.number,
  closeModalCallback: PropTypes.func.isRequired,
  updateCallback: PropTypes.func.isRequired,
}

const defaultProps = {
  idForEdit: null,
}

export const ExemptionAddEditModal = ({ isModalShown, idForEdit, closeModalCallback, updateCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(exemptionActionsLoading);

  const [exemption, setExemption] = useState(initialExemption);

  useEffect(() => {
    if (idForEdit) {
      dispatch(getExemptionForEdit(idForEdit)).then(({ payload }) => {
        const newInitialExemption = {
          regulation: payload.regulation?.id || '',
          regulatory_framework: payload.regulatory_framework?.id || '',
          substance: payload.substance,
          article: payload.article || '',
          reference: payload.reference || '',
          application: payload.application,
          expiration_date: payload.expiration_date || '',
          date_into_force: payload.date_into_force || '',
          status: payload.status,
          modified: payload.modified || dayjs().toISOString(),
        }

        setExemption(newInitialExemption)
      });
    } else {
      setExemption(initialExemption);
    }
  }, [dispatch, idForEdit]);

  const saveExemption = (values, isSaveAsNewVersion) => {
    const payload = {
      ...values,
      substance: values.substance?.id,
      expiration_date: values.expiration_date || null,
      date_into_force: values.date_into_force || null,
    };

    const afterActionCallback = () => {
      updateCallback();
      closeModalCallback();
    };

    const addNewExemptionAction = dataToSend => dispatch(addExemption(dataToSend)).then(() => afterActionCallback());
    const editExemptionAction = dataToSend =>
      dispatch(editExemption({ id: idForEdit, ...dataToSend })).then(() => afterActionCallback());

    if (!idForEdit) {
      // add new exemption
      addNewExemptionAction(payload);
    } else {
      if (isSaveAsNewVersion) {
        const updateCurrentExemption = {
          id: idForEdit,
          status: 'deleted',
          modified: dayjs().toISOString(),
          regulation: payload.regulation,
          regulatory_framework: payload.regulatory_framework,
        };
        const newExemption = {
          ...payload,
          status: 'active',
        };

        dispatch(editExemption(updateCurrentExemption)).then(() => addNewExemptionAction(newExemption));
      } else {
        editExemptionAction(payload);
      }
    }
  };

  const handleOnHide = () => closeModalCallback();

  const renderHeaderTitle = () => `${idForEdit ? 'Edit' : 'Add'} Exemption`;

  return isModalShown && (
    <Modal
      size="lg"
      show={isModalShown}
      onHide={handleOnHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}

      <Modal.Header>
        <Modal.Title id="example-modal-sizes-title-lg">
          {renderHeaderTitle()}
        </Modal.Title>
      </Modal.Header>

      <ExemptionForm
        exemption={exemption}
        saveExemption={saveExemption}
        onCancelCallback={closeModalCallback}
        actionsLoading={actionsLoading}
        isSaveAsNewAllowed={!!idForEdit}
      />
    </Modal>
  );
}

ExemptionAddEditModal.propTypes = propTypes;
ExemptionAddEditModal.defaultProps = defaultProps;
