import React from 'react';
import { Formik } from 'formik';
import PropTypes from 'prop-types';
import { Modal } from 'react-bootstrap';
import * as Yup from 'yup';

import { BUTTON } from '@common';
import { UiKitButton } from '@common/UIKit';

import { FamilyFieldsToEdit } from './FamilyFieldsToEdit';

const FamilySchema = Yup.object().shape({
  chemycal_id: Yup.string().nullable(),
  name: Yup.string()
    .nullable()
    .required('Name is required'),
});

const propTypes = {
  family: PropTypes.object.isRequired,
  saveFamily: PropTypes.func.isRequired,
  onCancelCallback: PropTypes.func.isRequired,
  actionsLoading: PropTypes.bool.isRequired,
  btnRef: PropTypes.object,
};

const defaultProps = {
  btnRef: null,
};

export const FamilyForm = ({ family, saveFamily, onCancelCallback, actionsLoading, btnRef }) => (
  <Formik enableReinitialize initialValues={family} validationSchema={FamilySchema} onSubmit={saveFamily}>
    {({ handleSubmit, setFieldValue, values, errors }) =>
      btnRef ? (
        <>
          <FamilyFieldsToEdit values={values} setFieldValue={setFieldValue} errors={errors} />
          <button type="submit" style={{ display: 'none' }} ref={btnRef} onClick={() => handleSubmit()} />
        </>
      ) : (
        <>
          <Modal.Body className="overlay overlay-block cursor-default">
            <FamilyFieldsToEdit values={values} setFieldValue={setFieldValue} />
          </Modal.Body>
          <Modal.Footer>
            <button type="button" onClick={onCancelCallback} className="btn btn-light btn-elevate">
              Back
            </button>

            <UiKitButton buttonType={BUTTON.SAVE} onClick={() => handleSubmit()} isLoading={actionsLoading} />
          </Modal.Footer>
        </>
      )
    }
  </Formik>
);

FamilyForm.propTypes = propTypes;
FamilyForm.defaultProps = defaultProps;
