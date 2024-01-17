import React from "react";
import { Modal } from "react-bootstrap";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { Input, Select } from "@metronic-partials/controls";

// Validation schema
const UserEditSchema = Yup.object().shape({
  first_name: Yup.string()
    .min(3, "Minimum 3 symbols")
    .max(50, "Maximum 50 symbols")
    .required("Firstname is required"),

  last_name: Yup.string()
    .min(3, "Minimum 3 symbols")
    .max(50, "Maximum 50 symbols")
    .required("Firstname is required"),

  email: Yup.string()
    .email("Invalid email")
    .required("Email is required"),

  country: Yup.string().required("Username is required"),
});

export function UserForm({
  user,
  actionsLoading,
  setShowUserAddModal,
  saveOrganizationUser,
  organizationId,
}) {
  const validatePassword = (password) => {
    let error;
    if (user.id === undefined && password.length < 8) {
      error = "Minimum 8 symbols";
    }
    return error;
  };
  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={{ ...user, password: "" }}
        validationSchema={UserEditSchema}
        onSubmit={(values) => {
          values.organization = organizationId
          saveOrganizationUser(values);
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
                  {/* First Name */}
                  <div className="col-lg-6">
                    <Field
                      name="first_name"
                      component={Input}
                      placeholder="First Name"
                      label="First Name"
                    />
                  </div>

                  <div className="col-lg-6">
                    <Field
                      name="last_name"
                      component={Input}
                      placeholder="Last Name"
                      label="Last Name"
                    />
                  </div>
                </div>

                <div className="form-group row">
                  <div className="col-lg-6">
                    <Field
                      name="city"
                      component={Input}
                      placeholder="City"
                      label="City"
                    />
                  </div>

                  <div className="col-lg-6">
                    <Field
                      name="country"
                      component={Input}
                      placeholder="Country"
                      label="Country"
                    />
                  </div>
                </div>

                <div className="form-group row">
                  <div className="col-lg-6">
                    <Field
                      autoComplete="off"
                      type="email"
                      name="email"
                      component={Input}
                      placeholder="Email"
                      label="Email"
                    />
                  </div>

                  <div className="col-lg-6">
                    <Select name="is_admin" label="User Role">
                      <option key="true" value={true}>
                        Org Admin
                      </option>
                      <option key="false" value={false}>
                        User
                      </option>
                    </Select>
                  </div>
                </div>

                <div className="form-group row">
                  <div className="col-lg-6">
                    <Select name="is_active" label="Status">
                      <option key="true" value={true}>
                        Active
                      </option>
                      <option key="false" value={false}>
                        Inactive
                      </option>
                    </Select>
                  </div>

                  {!user.id && (
                    <div className="col-lg-6">
                      <Field
                        autoComplete="new-password"
                        type="password"
                        name="password"
                        component={Input}
                        placeholder="Password"
                        label="Password"
                        validate={validatePassword}
                      />
                    </div>
                  )}
                </div>
              </Form>
            </Modal.Body>
            <Modal.Footer>
              <button
                type="button"
                onClick={() => setShowUserAddModal(false)}
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
