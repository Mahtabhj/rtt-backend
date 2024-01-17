import React from "react";
import { Modal } from "react-bootstrap";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

import { Input } from "@metronic-partials/controls";

// Validation schema
const UrlEditSchema = Yup.object().shape({
  text: Yup.string()
    .min(3, "Minimum 3 symbols")
    .required("Url is required"),
});

export function UrlForm({
  url,
  actionsLoading,
  setShowUrlAddModal,
  saveRegulationUrl,
}) {
  const handleOnSubmit = values => saveRegulationUrl(values);
  const handleOnClickCancel = () => setShowUrlAddModal(false);

  return (
    <Formik
      enableReinitialize
      initialValues={{ ...url }}
      validationSchema={UrlEditSchema}
      onSubmit={handleOnSubmit}
    >
      {({ handleSubmit, errors }) => (
        <>
          <Modal.Body className="overlay overlay-block cursor-default">
            <Form className="form form-label-right">
              <div className="form-group row">
                {/* First Name */}
                <div className="col-lg-12">
                  <Field
                    name="text"
                    component={Input}
                    placeholder="Url"
                    label="Url"
                    withFeedbackLabel={false}
                  />
                  {errors.text ? (<p className="text-danger">{errors.text}</p>) : null}
                </div>
              </div>

              <div className="form-group row">
                <div className="col-lg-12">
                  <label>Description</label>

                  <Field
                    name="description"
                    as="textarea"
                    className="form-control"
                    placeholder="Description"
                    label="description"
                  />
                </div>
              </div>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <button
              type="button"
              onClick={handleOnClickCancel}
              className="btn btn-light btn-elevate"
              disabled={actionsLoading}
            >
              Cancel
            </button>

            <button
              type="submit"
              onClick={() => handleSubmit()}
              className="btn btn-primary btn-elevate"
            >
              Save
            </button>
          </Modal.Footer>
        </>
      )}
    </Formik>
  );
}
