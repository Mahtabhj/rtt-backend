import React, { useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { Input, Select } from "@metronic-partials/controls";

// Validation schema
const SourceEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(150, "Maximum 150 symbols")
    .required("Name is required"),
  link: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(250, "Maximum 250 symbols")
    .required("Link is required"),
  type: Yup.string()
    .ensure()
    .required("Source type is required"),
  image: Yup.string()
    .ensure()
    .required("Source image is required"),
});

export function SourceEditForm({ source, btnRef, saveSource, sourceType }) {
  const [filename, setFilename] = useState("image");

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={source}
        validationSchema={SourceEditSchema}
        onSubmit={(values) => {
          saveSource(values);
        }}
      >
        {({ handleSubmit, setFieldValue }) => (
          <>
            <Form className="form form-label-right">
              <div className="form-group row">
                <div className="col-lg-6 mb-4">
                  <Field
                    name="name"
                    component={Input}
                    placeholder="Name"
                    label="Name *"
                  />
                </div>

                <div className="col-lg-6 mb-4">
                  <Field
                    name="link"
                    component={Input}
                    placeholder="Link"
                    label="Source Link *"
                  />
                </div>

                <div className="col-lg-6 mb-4">
                  <Select
                    name="type"
                    label="Source Type *"
                    withFeedbackLabel={false}
                  >
                    {sourceType.map((option, index) => (
                      <option key={option.id} value={sourceType[index].id}>
                        {option.name}
                      </option>
                    ))}
                  </Select>
                  <ErrorMessage name="type">
                    {(msg) => <div style={{ color: "red" }}>{msg}</div>}
                  </ErrorMessage>
                </div>

                <div className="col-lg-6 mb-4">
                  <label>Select Image *</label>
                  <input
                    id="image"
                    name="image"
                    type="file"
                    onChange={(event) => {
                      setFieldValue("image", event.currentTarget.files[0]);
                      setFilename("");
                    }}
                    className="form-control"
                  />
                  <ErrorMessage name="image">
                    {(msg) => <div style={{ color: "red" }}>{msg}</div>}
                  </ErrorMessage>
                  {source.id && filename && (
                    <a
                      href={source.image}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Current source image
                    </a>
                  )}
                </div>

                <div className="col-lg-12 mb-3">
                  <label>Description</label>
                  <Field
                    name="description"
                    as="textarea"
                    className="form-control"
                    placeholder="Description"
                    label="Source description"
                  />
                </div>
              </div>
              <button
                type="submit"
                style={{ display: "none" }}
                ref={btnRef}
                onSubmit={() => {
                  handleSubmit();
                }}
              ></button>
            </Form>
          </>
        )}
      </Formik>
    </>
  );
}
