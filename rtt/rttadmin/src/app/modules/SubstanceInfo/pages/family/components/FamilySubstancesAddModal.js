import React from 'react';
import { useDispatch, useSelector } from "react-redux";
import { Modal } from 'react-bootstrap';
import PropTypes from 'prop-types';
import { Form, Formik } from 'formik';

import { addFamilySubstances } from '../../../_redux/family/familyActions';
import { familyActionsLoading } from '../../../_redux/family/familySelectors';

import { BUTTON } from '@common';
import { UiKitButton, UiKitErrorMessage, UiKitProgressBar } from '@common/UIKit';
import { AddSubstanceManual } from '@common/RelatedSubstances/components/AddSubstanceManual';

const initialValues = { substances: [] };

const validate = values => {
  const errors = {};

  if (!values.substances.length) {
    errors.substances = 'Select at least one substance';
  }

  return errors;
};

const propTypes = {
  family: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
  }).isRequired,
  isModalShown: PropTypes.bool.isRequired,
  closeModalCallback: PropTypes.func.isRequired,
  updateCallback: PropTypes.func.isRequired,
}

export const FamilySubstancesAddModal = ({ family, isModalShown, closeModalCallback, updateCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(familyActionsLoading);

  const saveFamilySubstances = ({ substances }) => {
    const dataToSend = { id: family.id, substances: substances.map(({ id }) => id) }

    dispatch(addFamilySubstances(dataToSend)).then(() => {
      updateCallback();
      closeModalCallback();
    })
  };

  const handleOnHide = () => closeModalCallback();

  return (
    <Modal
      size="lg"
      show={isModalShown}
      onHide={handleOnHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      <UiKitProgressBar isLoading={actionsLoading} variant="query"/>

      <Modal.Header>
        <Modal.Title id="example-modal-sizes-title-lg">
          Add Substance to a Family: {family.name}
        </Modal.Title>
      </Modal.Header>

      <Formik
        initialValues={initialValues}
        validate={validate}
        onSubmit={saveFamilySubstances}
      >
        {({ handleSubmit, setFieldValue, values }) => (
          <>
            <Modal.Body className="overlay overlay-block cursor-default">
              <Form className="form form-label-right">
                <div className="form-group row">
                  <div className="col-lg-9">
                    <label>Substances</label>
                    <AddSubstanceManual
                      selected={values.substances}
                      onChange={substances => setFieldValue('substances', substances)}
                      isValuesShown
                    />
                    <UiKitErrorMessage name="substances" />
                  </div>
                </div>
              </Form>
            </Modal.Body>
            <Modal.Footer>
              <button
                type="button"
                onClick={closeModalCallback}
                className="btn btn-light btn-elevate"
              >
                Back
              </button>

              <UiKitButton buttonType={BUTTON.SAVE} onClick={handleSubmit} isLoading={actionsLoading} />
            </Modal.Footer>
          </>
        )}
      </Formik>
    </Modal>
  );
}

FamilySubstancesAddModal.propTypes = propTypes;
