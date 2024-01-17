import { Input } from "@metronic-partials/controls";
import { Field, Form, Formik } from "formik";
import React from "react";
import * as Yup from "yup";
import ReactSelect from "react-select";

// Validation schema
const IssuingBodyEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(150, "Maximum 150 symbols")
    .required("Name is required"),
});

export function IssuingBodyEditForm({
  issuingbody,
  btnRef,
  saveIssuingBody,
  regionOptions,
  urlList,
}) {
  return (
    <Formik
      enableReinitialize={true}
      initialValues={issuingbody}
      validationSchema={IssuingBodyEditSchema}
      onSubmit={values => saveIssuingBody(values)}
    >
      {({ handleSubmit, setFieldValue, values }) => (
        <Form className="form form-label-right">
          <div className="form-group mb-2 row">
            <div className="col-lg-12">
              <Field
                name="name"
                component={Input}
                withFeedbackLabel={false}
                placeholder="Name"
                label="Name *"
              />
            </div>
          </div>

          <div className="form-group mb-2 row">
            <div className="col-lg-6">
              <Field
                name="url"
                component={Input}
                withFeedbackLabel={false}
                placeholder="Url"
                label="Url"
              />
            </div>

            <div className=" col-lg-6 mb-2 form-group">
              <label>Region</label>
              <ReactSelect
                name="region"
                options={regionOptions}
                value={regionOptions.find(option => option.id === values.region)}
                getOptionValue={option => option.id}
                getOptionLabel={option => option.name}
                onChange={value => setFieldValue("region", value.id)}
                blurInputOnSelect
                captureMenuScroll
                closeMenuOnSelect
                isSearchable
              />
            </div>
          </div>

          <div className="form-group mb-2 row">
            <div className="col-lg-12">
              <label>Description</label>
              <Field
                name="description"
                as="textarea"
                className="form-control"
                placeholder="Description"
              />
            </div>
          </div>

          <button
            type="submit"
            style={{ display: "none" }}
            ref={btnRef}
            onSubmit={() => handleSubmit()}
          />
        </Form>
      )}
    </Formik>
  );
}
