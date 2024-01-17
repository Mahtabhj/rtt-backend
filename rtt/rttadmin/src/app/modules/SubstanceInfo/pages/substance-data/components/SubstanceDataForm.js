import React from 'react';
import { Formik } from 'formik';
import PropTypes from 'prop-types';
import { Modal } from 'react-bootstrap';
import * as Yup from 'yup';

import { SubstanceDataFieldsToEdit } from './SubstanceDataFieldsToEdit';

const SubstanceDataAddSchema = Yup.object().shape({
  substance: Yup.object()
    .nullable()
    .required('Substance is required'),
  property: Yup.object()
    .nullable()
    .required('Property is required'),
  property_data_points: Yup.array().notRequired(),
});

const propTypes = {
  substanceData: PropTypes.object.isRequired,
  saveSubstanceData: PropTypes.func.isRequired,
  onCancelCallback: PropTypes.func.isRequired,
  isEdit: PropTypes.bool.isRequired,
  actionsLoading: PropTypes.bool.isRequired,
};

export const SubstanceDataForm = ({ substanceData, saveSubstanceData, onCancelCallback, isEdit, actionsLoading }) => {
  const handleOnSubmit = values => saveSubstanceData(values, false);

  return (
    <Formik
      enableReinitialize
      initialValues={substanceData}
      validationSchema={SubstanceDataAddSchema}
      onSubmit={handleOnSubmit}
    >
      {({ handleSubmit, setFieldValue, values }) => (
        <>
          <Modal.Body className="overlay overlay-block cursor-default">
            <SubstanceDataFieldsToEdit values={values} setFieldValue={setFieldValue} isEdit={isEdit} />
          </Modal.Body>
          <Modal.Footer>
            <button type="button" onClick={onCancelCallback} className="btn btn-light btn-elevate">
              Back
            </button>

            <button
              type="submit"
              onClick={() => handleSubmit()}
              className="btn btn-primary btn-elevate"
              style={{ minWidth: "100px" }}
            >
              Save
              {actionsLoading && <span className="ml-3 spinner spinner-white" />}
            </button>

            {isEdit && (
              <button
                type="button"
                onClick={() => saveSubstanceData(values, true)}
                className="btn btn-primary"
                style={{ minWidth: '210px' }}
              >
                Save as new version
                {actionsLoading && (<span className="ml-3 spinner spinner-white"/>)}
              </button>
            )}
          </Modal.Footer>
        </>
      )}
    </Formik>
  );
};

SubstanceDataForm.propTypes = propTypes;
