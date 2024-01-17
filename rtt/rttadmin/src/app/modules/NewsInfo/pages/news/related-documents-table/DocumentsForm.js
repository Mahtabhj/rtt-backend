import React, { useState, useEffect } from "react";
import { Modal } from "react-bootstrap";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { Input, Select } from "@metronic/_partials/controls";
import RichTextEditor from 'react-rte';

// Validation schema
const DocumentsEditSchema = Yup.object().shape({
  title: Yup.string()
    .min(3, "Minimum 3 symbols")
    .max(150, "Maximum 150 symbols")
    .required("Title is required"),
  type: Yup.string()
    .ensure()
    .required("Document type is required"),
  attachment: Yup.string()
    .ensure()
    .required("Attachment is required"),
});

export function DocumentsForm({
  documents,
  actionsLoading,
  setShowDocumentsAddModal,
  saveNewsRelatedDocuments,
  documentTypeList,
  isSaving,
}) {
  const [filename, setFilename] = useState(documents.attachment);

  useEffect(() => {
    setFilename(documents.attachment || null);
  }, [documents]);

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={documents}
        validationSchema={DocumentsEditSchema}
        onSubmit={(values) => {
          saveNewsRelatedDocuments({
            ...values,
            type: values.type?.id || values.type,
          });
        }}
      >
        {({ handleSubmit, errors, setFieldValue, values }) => (
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
                      name="title"
                      component={Input}
                      placeholder="Title"
                      label="Title *"
                      withFeedbackLabel={false}
                    />
                    {errors.title ? (
                      <p className="text-danger"> {errors.title} </p>
                    ) : null}
                  </div>

                  <div className="col-lg-6">
                    <Select
                      name="type"
                      label="Type *"
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
                      {(msg) => <div style={{ color: "red" }}>{msg}</div>}
                    </ErrorMessage>
                  </div>
                </div>

                <div className="form-group row">
                  <div className="col-lg-12">
                    <label>Attachment *</label>
                    <input
                      id="attachment"
                      name="attachment"
                      type="file"
                      onChange={(event) => {
                        setFieldValue(
                          "attachment",
                          event.currentTarget.files[0]
                        );
                        setFilename("");
                      }}
                      className="form-control"
                    />
                    <ErrorMessage name="attachment">
                      {(msg) => <div style={{ color: "red" }}>{msg}</div>}
                    </ErrorMessage>

                    {filename && (
                      <a
                        href={filename}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          width: '100%',
                          whiteSpace: 'nowrap',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          position: 'absolute',
                          bottom: '-22px'
                        }}
                      >
                        {filename.split("?")[0]}
                      </a>
                    )}
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
                onClick={() => setShowDocumentsAddModal(false)}
                className="btn btn-light btn-elevate"
              >
                Cancel
              </button>
              <> </>
              <button
                type="submit"
                disabled={isSaving}
                onClick={() => handleSubmit()}
                style={{ width: '100px' }}
                className="btn btn-primary btn-elevate"
              >
                Save
                {isSaving && (<span className="ml-3 spinner spinner-white" />)}
              </button>
            </Modal.Footer>
          </>
        )}
      </Formik>
    </>
  );
}
