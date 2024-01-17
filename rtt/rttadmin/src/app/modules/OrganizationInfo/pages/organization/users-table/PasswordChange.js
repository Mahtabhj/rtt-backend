import React from "react";
import { Modal } from "react-bootstrap";
import { Formik, Form, Field } from "formik";
import { Input } from "@metronic-partials/controls";

export function PasswordChangeForm({
  actionsLoading,
  setShowUserPasswordChangeModal,
  saveNewPassword,
}) {

  const validatePassword = (password) => {
    let error;
    if (password.length < 8) {
      error = "Minimum 8 symbols";
    }
    return error;
  };

  return (
    <>
      <Formik
        initialValues={{ password: "" }}
        onSubmit={(values) => {
          saveNewPassword(values);
        }}
      >
        {({ handleSubmit }) => (
          <>
            <Modal.Body className="overlay overlay-block cursor-default">
              {actionsLoading && (
                <div className="overlay-layer bg-transparent">
                  <div className="spinner spinner-lg spinner-success" />
                </div>
              )}
              <Form className="form form-label-right">
                <div className="form-group row">
                  <div className="col-lg-6">
                    <Field
                      type="password"
                      name="password"
                      component={Input}
                      placeholder="Password"
                      label="Password"
                      validate={validatePassword}
                    />
                  </div>
                </div>
              </Form>
            </Modal.Body>
            <Modal.Footer>
              <button
                type="button"
                onClick={() => setShowUserPasswordChangeModal(false)}
                className="btn btn-light btn-elevate"
              >
                Cancel
              </button>
              <> </>
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
    </>
  );
}
