import React from "react";
import { Modal } from "react-bootstrap";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

import { Input } from "@metronic-partials/controls";

// Validation schema
const LinkEditSchema = Yup.object().shape({
  text: Yup.string()
    .min(3, "Minimum 3 symbols")
    .required("Name is required"),
});

export function LinkForm({
  link,
  actionsLoading,
  setShowLinkAddModal,
  saveRegulatoryFrameworkLink,
}) {
  return (
    <Formik
      enableReinitialize
      initialValues={{ ...link }}
      validationSchema={LinkEditSchema}
      onSubmit={(values) => saveRegulatoryFrameworkLink(values)}
    >
      {({ handleSubmit }) => (
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
              onClick={() => setShowLinkAddModal(false)}
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
