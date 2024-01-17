import { Input } from "@metronic-partials/controls";
import * as regulatoryFrameworkApiService from "@redux-regulation/regulatory-framework/regulatoryFrameworkApiService";
import { ErrorMessage, Field, Form, Formik } from "formik";
import React, { useEffect, useState } from "react";
import { Modal } from "react-bootstrap";
import Select from "react-select";
import * as Yup from "yup";
import RichTextEditor from 'react-rte';

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
  saveRegulatoryFrameworkRelatedDocuments,
  isSaving,
}) {
  const [typeOptions, setTypeOptions] = useState([]);
  const [typeSelected, setTypeSelected] = useState([]);
  const [filename, setFilename] = useState(documents.attachment);

  useEffect(() => {
    setFilename(documents.attachment || null);
  }, [documents]);

  useEffect(() => {
    // todo use commonApi
    regulatoryFrameworkApiService
      .getDocumentTypeList()
      .then((response) => {
        const typeOption = response.data.results.map((option) => {
          return { value: option.id, label: option.name };
        });

        if (documents.id) {
          setTypeSelected(
            typeOption.find((type) => type.value === documents.type.id)
          );
        } else {
          setTypeSelected(typeOption[0]);
        }

        setTypeOptions(typeOption);
      })
      .catch((error) => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={{ ...documents }}
        validationSchema={DocumentsEditSchema}
        onSubmit={(values) => {
          values.type = typeSelected.value;
          saveRegulatoryFrameworkRelatedDocuments(values);
        }}
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
                          options={typeOptions}
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
                onClick={() => setShowDocumentsAddModal(false)}
                className="btn btn-light btn-elevate"
                disabled={isSaving}
              >
                Cancel
              </button>

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
