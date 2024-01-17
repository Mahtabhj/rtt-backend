import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Modal } from "react-bootstrap";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import { toast } from "react-toastify";

import { addLimit, deleteLimits, editLimits, getLimitForEdit } from "../../../_redux/limit/limitActions";
import { limitActionsLoading } from "../../../_redux/limit/limitSelectors";

import { ModalProgressBar } from "@metronic-partials/controls";

import { prepareDateForRequest, DATE_FORMAT_FOR_REQUEST } from "@common";

import { LimitForm } from "./LimitForm";

const bulkEditFields = ['substance', 'scope', 'limit_value', 'measurement_limit_unit', 'limit_note', 'status', 'date_into_force', 'modified'];

const initialLimit = {
  regulation: '',
  regulatory_framework: '',
  substance: null,
  scope: '',
  limit_value: '',
  measurement_limit_unit: '',
  limit_note: '',
  additional_attribute_values: [],
  status: 'active',
  date_into_force: '',
  modified: '',
};

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  idsForEdit: PropTypes.arrayOf(PropTypes.number.isRequired),
  closeModalCallback: PropTypes.func.isRequired,
  updateCallback: PropTypes.func.isRequired,
}

const defaultProps = {
  idsForEdit: [],
}

export const LimitAddEditModal = ({ isModalShown, idsForEdit, closeModalCallback, updateCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(limitActionsLoading);

  const [limit, setLimit] = useState(initialLimit);

  useEffect(() => {
    if (idsForEdit.length === 1) {
      const [limitId] = idsForEdit;

      dispatch(getLimitForEdit(limitId)).then(({ payload: { limit_attributes, ...limitForEdit } }) => {
        const newInitialLimit = {
          ...limitForEdit,
          regulation: limitForEdit.regulation?.id || '',
          regulatory_framework: limitForEdit.regulatory_framework?.id || '',
          additional_attribute_values: limit_attributes,
          date_into_force: limitForEdit.date_into_force || '',
          modified: limitForEdit.modified || '',
        }

        setLimit(newInitialLimit)
      });
    } else {
      setLimit(initialLimit);
    }
  }, [dispatch, idsForEdit]);

  const saveLimit = (values, isSaveAsNewVersion) => {
    const additionalAttributeValues = values.additional_attribute_values.map(({ id, value }) => ({
      attribute_id: id,
      value,
    }));

    const remainedAdditionalAttributesIds = additionalAttributeValues.map(({ attribute_id }) => attribute_id);

    const removedAdditionalAttributes = limit.additional_attribute_values
      .filter(({ id }) => !remainedAdditionalAttributesIds.includes(id))
      .map(({ id }) => id);

    const payload = {
      ...values,
      substance: values.substance?.id,
      date_into_force: values.date_into_force || null,
      modified: prepareDateForRequest(values.modified),
      additional_attribute_values: additionalAttributeValues,
      removed_additional_attributes: removedAdditionalAttributes,
    };

    const afterActionCallback = () => {
      updateCallback();
      closeModalCallback();
    };

    const addNewLimitAction = dataToSend => dispatch(addLimit(dataToSend)).then(() => afterActionCallback());
    const editLimitsAction = dataToSend => dispatch(editLimits(dataToSend)).then(() => afterActionCallback());

    if (!idsForEdit.length) {
      // add new limit
      addNewLimitAction(payload);
    } else if (idsForEdit.length === 1) {
      // edit limit
      payload.limits = idsForEdit;

      if (isSaveAsNewVersion) {
        const deleteCurrentLimit = {
          limits: payload.limits,
          date: dayjs().format(DATE_FORMAT_FOR_REQUEST),
        };
        const newLimit = {
          ...payload,
          status: 'active',
        };

        dispatch(deleteLimits(deleteCurrentLimit)).then(() => addNewLimitAction(newLimit));
      } else {
        // const additional_attribute_values = payload.additional_attribute_values; configure additional attributes if needed
        editLimitsAction(payload);
      }
    } else {
      // bulk edit
      const bulkEditData = { limits: idsForEdit };
      let isAnyData = false;

      bulkEditFields.forEach(key => {
        if (payload[key]) {
          bulkEditData[key] = payload[key];
          isAnyData = true;
        }
      })

      isAnyData ? editLimitsAction(bulkEditData) : toast.info('No data filled');
    }
  };

  const handleOnHide = () => closeModalCallback();

  const isBulkEdit = idsForEdit.length > 1;

  const renderHeaderTitle = () => {
    if (isBulkEdit) {
      return `Apply the following change to ${idsForEdit.length} records selected`
    } else {
      return `${idsForEdit.length ? 'Edit' : 'Add'} Limit`
    }
  };

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

      <LimitForm
        limit={limit}
        saveLimit={saveLimit}
        onCancelCallback={closeModalCallback}
        actionsLoading={actionsLoading}
        isSaveAsNewAllowed={idsForEdit.length === 1}
        isFullForm={!isBulkEdit}
      />
    </Modal>
  );
}

LimitAddEditModal.propTypes = propTypes;
LimitAddEditModal.defaultProps = defaultProps;
