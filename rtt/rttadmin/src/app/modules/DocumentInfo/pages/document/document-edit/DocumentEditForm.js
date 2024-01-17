import React, { useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { Input, Select } from "@metronic-partials/controls";

// Validation schema
const DocumentEditSchema = Yup.object().shape({
  title: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(150, "Maximum 150 symbols")
    .required("Name is required"),
  type: Yup.string()
    .ensure()
    .required("Type is required"),
  attachment: Yup.string()
    .ensure()
    .required("File is required"),
});

export function DocumentEditForm({
  document,
  btnRef,
  saveDocument,
  documentTypeList,
}) {
  const [file, setFile] = useState(null);

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={document}
        validationSchema={DocumentEditSchema}
        onSubmit={(values) => {
          saveDocument(values);
        }}
      >
        {({ handleSubmit, setFieldValue, errors }) => (
          <>
            <Form className="form form-label-right">
              <div className="form-group row">
                <div className="col-lg-6 mb-4">
                  <Field
                    name="title"
                    component={Input}
                    placeholder="Name"
                    label="Name *"
                  />
                </div>
                <div className="col-lg-6 mb-4">
                  <Select
                    name="type"
                    label="Document Type *"
                    withFeedbackLabel={false}
                  >
                    {documentTypeList.map((option, index) => (
                      <option
                        key={option.id}
                        value={documentTypeList[index].id}
                      >
                        {option.name}
                      </option>
                    ))}
                  </Select>
                  <ErrorMessage name="type">
                    {(msg) => <div className="text-danger">{msg}</div>}
                  </ErrorMessage>
                </div>
              </div>

              <div className="form-group mb-2 row">
                <div className="col-lg-6">
                  <div className="row">
                    <div className="col-lg-12 mb-4">
                      <label>Select File *</label>
                      <input
                        id="attachment_file"
                        name="attachment"
                        type="file"
                        onChange={(event) => {
                          setFieldValue(
                            "attachment",
                            event.currentTarget.files[0]
                          );
                          setFile(
                            URL.createObjectURL(event.currentTarget.files[0])
                          );
                        }}
                        className="form-control"
                      />
                      {errors.attachment ? (
                        <div className="text-danger">{errors.attachment}</div>
                      ) : null}
                    </div>

                    <div className="col-lg-12 mb-3">
                      <Field
                        name="description"
                        as="textarea"
                        className="form-control"
                        placeholder="Description"
                        label="Document description"
                      />
                    </div>
                  </div>
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
                  ) : document.attachment ? (
                    <img
                      className="ml-auto 20"
                      height="150"
                      width="300"
                      src={document.attachment}
                      alt="cover"
                    ></img>
                  ) : null}
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
