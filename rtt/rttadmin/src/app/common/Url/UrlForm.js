import React from "react";
import { Modal } from "react-bootstrap";
import RichTextEditor from "react-rte";
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
  saveUrl,
}) {
  const handleOnSubmit = (values) => saveUrl(values);
  const handleOnClickCancel = () => setShowUrlAddModal(false);

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={{ ...url }}
        validationSchema={UrlEditSchema}
        onSubmit={handleOnSubmit}
      >
        {({ handleSubmit,
            errors,
            setFieldValue, handleChange,
            values }) => (
          <>
            <Modal.Body className="overlay overlay-block cursor-default">
              {actionsLoading && (
                <div className="overlay-layer bg-transparent">
                  <div className="spinner spinner-lg spinner-success" />
                </div>
              )}
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

                    <RichTextEditor
                      value={values.description}
                      onChange={(value) => setFieldValue("description", value)}
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
              >
                Cancel
              </button>
              <> </>
              <button
                type="submit"
                onClick={handleSubmit}
                className="btn btn-primary btn-elevate"
              >
                Save
              </button>
            </Modal.Footer>
          </>
        )}
      </Formik>
    </>
  );
}
