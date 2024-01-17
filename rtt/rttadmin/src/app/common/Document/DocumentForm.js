import React, { useState, useEffect } from "react";
import RichTextEditor from 'react-rte';
import Select from "react-select";
import { Modal } from "react-bootstrap";
import { ErrorMessage, Field, Form, Formik } from "formik";
import * as Yup from "yup";

import { Input } from "@metronic-partials/controls";
import { getDocumentTypeList } from "@redux/commonApiService";

// Validation schema
const DocumentsEditSchema = Yup.object().shape({
  title: Yup.string()
    .min(3, "Minimum 3 symbols")
    .max(150, "Maximum 150 symbols")
    .required("Document title is required"),
  attachment: Yup.string()
    .ensure()
    .required("Attachment is required"),
});

export function DocumentsForm({
  documents,
  actionsLoading,
  setShowDocumentsAddModal,
  saveRelatedDocuments,
  isSaving,
}) {
  const [documentTypeOptions, setDocumentTypeOptions] = useState([]);
  const [typeSelected, setTypeSelected] = useState([]);
  const [filename, setFilename] = useState(documents.attachment);

  useEffect(() => {
    setFilename(documents.attachment || null);
  }, [documents]);

  useEffect(() => {
    getDocumentTypeList()
      .then((response) => setDocumentTypeOptions(
        response.data.results.map((option) => (
          { value: option.id, label: option.name }
        ))
      ))
      .catch((error) => {console.error(error)})
  }, []);

  useEffect(() => {
    if (documents.id) {
      const type = documentTypeOptions?.find(
        (type) => type.value === documents.type.id
      );
      setTypeSelected(type);
    } else {
      setTypeSelected(documentTypeOptions[0]);
    }
  }, [documentTypeOptions]);

  const handleOnSubmit = (values) => {
    values.type = { id: typeSelected.value, name: typeSelected.label };
    saveRelatedDocuments(values, typeSelected);
  };

  const handleOnClickCancel = () => setShowDocumentsAddModal(false);

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={{ ...documents }}
        validationSchema={DocumentsEditSchema}
        onSubmit={handleOnSubmit}
      >
        {({ handleSubmit, errors, setFieldValue, handleChange, values }) => (
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
                      placeholder="title"
                      label="Title"
                      withFeedbackLabel={false}
                    />
                    {errors.title ? (
                      <p className="text-danger"> {errors.title} </p>
                    ) : null}
                  </div>

                  <div className="col-lg-6">
                    <label>Type</label>
                    <Field
                      name="type"
                      component={({ field, form }) => (
                        <Select
                          isMulti={false}
                          options={documentTypeOptions}
                          value={typeSelected}
                          onChange={(e) => setTypeSelected(e)}
                        />
                      )}
                    />
                  </div>
                </div>

                <div className="form-group row">
                  <div className="col-lg-12">
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

                <div className="form-group row position-relative zindex-0">
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
                disabled={isSaving}
                onClick={handleSubmit}
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
