import React  from "react";
import { Formik } from "formik";
import PropTypes from "prop-types";
import { Modal } from "react-bootstrap";
import * as Yup from "yup";

import { LimitFieldsToEdit } from "./LimitFieldsToEdit";

const LimitAddSchema = Yup.object().shape({
  regulation: Yup.string()
    .when(['regulatory_framework'], {
      is: regulatoryFramework => !regulatoryFramework,
      then: Yup.string().required('One of R or RF is required'),
      otherwise: Yup.string().notRequired(),
    }),
  regulatory_framework: Yup.string()
    .when(['regulation'], {
      is: regulation => !regulation,
      then: Yup.string().required('One of R or RF is required'),
      otherwise: Yup.string().notRequired(),
    }),
  substance: Yup.object().nullable().required("Substance is required"),
  scope: Yup.string().notRequired(),
  limit_value: Yup.string().required('Limit value is required'),
  measurement_limit_unit: Yup.string().notRequired(),
  limit_note: Yup.string().notRequired(),
  additional_attribute_values: Yup.array().notRequired(),
  status: Yup.string().required('Status is required'),
  date_into_force: Yup.string().notRequired(),
  modified: Yup.string().notRequired(),
}, [['regulation', 'regulatory_framework']]);

const LimitEditSchema = Yup.object().shape({
  substance: Yup.object().nullable().notRequired(),
  scope: Yup.string().notRequired(),
  limit_value: Yup.string().notRequired(),
  measurement_limit_unit: Yup.string().notRequired(),
  limit_note: Yup.string().notRequired(),
  status: Yup.string().notRequired(),
  date_into_force: Yup.string().notRequired(),
  modified: Yup.string().notRequired(),
});

const propTypes = {
  limit: PropTypes.object.isRequired,
  saveLimit: PropTypes.func.isRequired,
  onCancelCallback: PropTypes.func.isRequired,
  actionsLoading: PropTypes.bool.isRequired,
  isSaveAsNewAllowed: PropTypes.bool.isRequired,
  isFullForm: PropTypes.bool.isRequired,
}

export const LimitForm = ({ limit, saveLimit, onCancelCallback, actionsLoading, isSaveAsNewAllowed, isFullForm }) => {
  const handleOnSubmit = values => saveLimit(values, false);

  return (
    <Formik
      enableReinitialize
      initialValues={{ ...limit, status: isFullForm ? limit.status : '' }}
      validationSchema={isFullForm ? LimitAddSchema : LimitEditSchema}
      onSubmit={handleOnSubmit}
    >
      {({ handleSubmit, setFieldValue, values }) => (
        <>
          <Modal.Body className="overlay overlay-block cursor-default">
            <LimitFieldsToEdit
              values={values}
              setFieldValue={setFieldValue}
              isFullForm={isFullForm}
            />
          </Modal.Body>
          <Modal.Footer>
            <button
              type="button"
              onClick={onCancelCallback}
              className="btn btn-light btn-elevate"
            >
              Back
            </button>

            <button
              type="submit"
              onClick={() => handleSubmit()}
              className="btn btn-primary btn-elevate"
              style={{ minWidth: '100px' }}
            >
              Save
              {actionsLoading && (<span className="ml-3 spinner spinner-white" />)}
            </button>

            {isSaveAsNewAllowed && (
              <button
                type="button"
                onClick={() => saveLimit(values, true)}
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
}

LimitForm.propTypes = propTypes;
