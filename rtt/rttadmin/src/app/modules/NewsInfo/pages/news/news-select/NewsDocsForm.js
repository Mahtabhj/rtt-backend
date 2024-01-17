import React, { useState } from "react";
import { ErrorMessage, Form, Formik } from "formik";
import ReactSelect from "react-select";
import Spinner from "react-bootstrap/Spinner";
import * as Yup from "yup";

import * as newsApiService from "@redux-news/news/newsApiService";

import "pure-react-carousel/dist/react-carousel.es.css";

// Validation schema
const docItemSchema = Yup.object().shape({
  description: Yup.string(),
  link: Yup.string(),
  title: Yup.string().ensure().required("Document name is required"),
  type: Yup.string().ensure().required("Document type is required"),
});

export const NewsDocsForm = ({ newsId, saveNews, newsDocs, newsDocTypes }) => (
  <>
    <h4 style={{ marginTop: '40px' }}>The news contains following documents:</h4>

    {newsDocs.map((newsDoc, index) => (
      <div className="form-group" key={index}>
        <DocForm
          newsDoc={newsDoc}
          newsDocTypes={newsDocTypes}
          newsId={newsId}
          saveNews={saveNews}
        />
      </div>
    ))}
  </>
);

const DocForm = ({ newsDoc, newsDocTypes, newsId, saveNews }) => {
  const initialDoc = {
    title: newsDoc.title,
    description: '',
    type: '',
    link: newsDoc.link,
  };

  const [inputDisabled, setInputDisabled] = useState(false);
  const [loading, setLoading] = useState(false);

  const saveLink = doc => {
    setLoading(true);
    newsApiService
      .saveNewsDoc(newsId, { ...doc, type: doc.type.id })
      .then(({ data }) => {
        saveNews({ doc, data }, "body");
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setLoading(false);
      });
  };

  const disableFields = () => setInputDisabled(prevState => !prevState);

  return (
    <Formik
      initialValues={initialDoc}
      validationSchema={docItemSchema}
      onSubmit={saveLink}
      enableReinitialize
    >
      {({ values, setFieldValue, handleSubmit }) => {
        const handleOnChange = field => ({ target: { value } }) => setFieldValue(field, value);
        const handleSelectOnChange = value => setFieldValue('type', value);
        const handleOnSubmit = () => handleSubmit();

        return (
          <Form>
            <div className="form-group row pt-10">
              <div className="col-lg-12">
                <a href={newsDoc.link} target="_blank" rel="noopener noreferrer"
                   className="h3 text-primary">{newsDoc.title}</a>
              </div>
            </div>

            <div className="form-group row">
              <div className="col-lg-12">
                <label>Document name</label>

                <input
                  disabled={inputDisabled}
                  type="text"
                  className="form-control"
                  name="title"
                  placeholder="Title"
                  value={values.title}
                  onChange={handleOnChange('title')}
                />

                <ErrorMessage name="title">
                  {(msg) => <div style={{ color: "red" }}>{msg}</div>}
                </ErrorMessage>
              </div>
            </div>

            <div className="form-group row">
              <div className="col-lg-12">
                <label>Document description</label>

                <input
                  disabled={inputDisabled}
                  type="textarea"
                  className="form-control"
                  name="description"
                  placeholder="Description"
                  value={values.description}
                  onChange={handleOnChange('description')}
                />
              </div>
            </div>

            <div className="form-group row">
              <div className="col-lg-6">
                <label>Document type</label>

                <ReactSelect
                  name="type"
                  value={values.type}
                  getOptionLabel={option => option.name}
                  getOptionValue={option => option.id}
                  onChange={handleSelectOnChange}
                  options={newsDocTypes}
                />

                <ErrorMessage name="type">
                  {(msg) => <div style={{ color: "red" }}>{msg}</div>}
                </ErrorMessage>
              </div>
            </div>

            <div className="form-group row">
              <div className="col-lg-12">
                <button
                  disabled={loading}
                  type="submit"
                  onClick={handleOnSubmit}
                  className="btn btn-primary "
                >
                  {loading && (
                    <Spinner
                      as="span"
                      animation="grow"
                      size="sm"
                      role="status"
                      aria-hidden="true"
                    />
                  )}
                  Save and replace link
                </button>

                <button
                  type="button"
                  onClick={disableFields}
                  className="btn btn-danger"
                  style={{ marginLeft: '10px' }}
                >
                  {loading && (
                    <Spinner
                      as="span"
                      animation="grow"
                      size="sm"
                      role="status"
                      aria-hidden="true"
                    />
                  )}

                  {inputDisabled ? 'Allow editing' : 'Keep external link'}
                </button>
              </div>
            </div>
          </Form>
        )
      }}
    </Formik>
  );
};
