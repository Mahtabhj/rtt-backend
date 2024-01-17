import React, { useState } from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { Input, Select } from "@metronic-partials/controls";

// Validation schema
const OrganizationEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(150, "Maximum 150 symbols")
    .required("Name is required"),
});

export function OrganizationEditForm({
  organization,
  btnRef,
  saveOrganization,
}) {
  const [file, setFile] = useState(null);

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={organization}
        validationSchema={OrganizationEditSchema}
        onSubmit={(values) => {
          saveOrganization(values);
        }}
      >
        {({ handleSubmit, setFieldValue, errors }) => (
          <>
            <Form className="form form-label-right">
              <div className="form-group row">
                <div className="col-lg-6">
                  <Field
                    name="name"
                    component={Input}
                    placeholder="Name"
                    label="Organization Name"
                  />
                </div>
                <div className="col-lg-6">
                  <Select name="active" label="Status">
                    <option key="Active" value={true}>
                      Active
                    </option>
                    <option key="Deactivated" value={false}>
                      Deactivated
                    </option>
                  </Select>
                </div>
              </div>

              <div className="form-group row">
                <div className="col-lg-6">
                  <Field
                    name="country"
                    component={Input}
                    placeholder="Country"
                    label="Organization Country"
                  />
                </div>
                <div className="col-lg-6">
                  <Field
                    name="address"
                    component={Input}
                    placeholder="Billing Address"
                    label="Organization Billing Address"
                  />
                </div>
              </div>

              <div className="form-group row">
                <div className="col-lg-6">
                  <Field
                    name="tax_code"
                    component={Input}
                    placeholder="Tax Code"
                    label="Organization Tax Code"
                  />
                </div>

                <div className="col-lg-6">
                  <Field
                    name="primary_color"
                    component={Input}
                    placeholder="Primary Color"
                    label="Primary Color"
                  />
                </div>
              </div>

              <div className="form-group row">
                <div className="col-lg-6">
                  <Field
                    name="secondary_color"
                    component={Input}
                    placeholder="Secondary Color"
                    label="Secondary Color"
                  />
                </div>

                <div className="col-lg-6">
                  <Field
                    name="session_timeout"
                    component={Input}
                    placeholder="Session Timeout"
                    label="Session Timeout"
                  />
                </div>
              </div>

              <div className="form-group row">
                <div className="col-lg-6">
                  <Field
                    name="password_expiration"
                    component={Input}
                    placeholder="Password Expiration"
                    label="Password Expiration"
                  />
                </div>
              </div>

              <div className="form-group row">
                <div className="col-lg-6">
                      <label>Select Logo</label>
                      <input
                        id="logo"
                        name="logo"
                        type="file"
                        onChange={(event) => {
                          setFieldValue("logo", event.currentTarget.files[0]);
                          setFile(URL.createObjectURL(event.currentTarget.files[0]));
                        }}
                        className="form-control"
                      />
                      {errors.logo ? (
                        <div className="text-danger">{errors.logo}</div>
                      ) : null}
                    </div>

                <div className="col-lg-6">
                  {file ? (
                    <img
                      className="ml-auto 10"
                      height="150"
                      width="300"
                      src={file}
                      alt="cover"
                    ></img>
                  ) : organization.logo ? (
                    <img
                      className="ml-auto 20"
                      height="150"
                      width="300"
                      src={organization.logo}
                      alt="cover"
                    ></img>
                  ) : null}
                </div>
              </div>

              <button
                type="submit"
                style={{ display: "none" }}
                ref={btnRef}
                onSubmit={() => handleSubmit()}
              ></button>
            </Form>
          </>
        )}
      </Formik>
    </>
  );
}
