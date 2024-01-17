import React  from "react";
import { Formik } from "formik";
import PropTypes from "prop-types";
import { Modal } from "react-bootstrap";
import * as Yup from "yup";

import { ExemptionFieldsToEdit } from "./ExemptionFieldsToEdit";

const ExemptionSchema = Yup.object().shape({
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
  article: Yup.string().notRequired(),
  reference: Yup.string().notRequired(),
  application: Yup.string().notRequired(),
  expiration_date: Yup.string().notRequired(),
  date_into_force: Yup.string().notRequired(),
  status: Yup.string().required('Status is required'),
  modified: Yup.string().required('Updated on is required'),
}, [['regulation', 'regulatory_framework']]);

const propTypes = {
  exemption: PropTypes.object.isRequired,
  saveExemption: PropTypes.func.isRequired,
  onCancelCallback: PropTypes.func.isRequired,
  actionsLoading: PropTypes.bool.isRequired,
  isSaveAsNewAllowed: PropTypes.bool.isRequired,
}

export const ExemptionForm = ({ exemption, saveExemption, onCancelCallback, actionsLoading, isSaveAsNewAllowed }) => {
  const handleOnSubmit = values => saveExemption(values, false);

  return (
    <Formik
      enableReinitialize
      initialValues={exemption}
      validationSchema={ExemptionSchema}
      onSubmit={handleOnSubmit}
    >
      {({ handleSubmit, setFieldValue, values }) => (
        <>
          <Modal.Body className="overlay overlay-block cursor-default">
            <ExemptionFieldsToEdit
              values={values}
              setFieldValue={setFieldValue}
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
                onClick={() => saveExemption(values, true)}
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

ExemptionForm.propTypes = propTypes;
