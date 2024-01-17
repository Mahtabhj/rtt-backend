import React, { useEffect, useRef } from "react";
import RichTextEditor from "react-rte";
import ReactSelect from "react-select";
import { FormCheck } from 'react-bootstrap';
import { Form, Field, ErrorMessage } from "formik";

import { Input, DatePickerField, Select } from "@metronic-partials/controls";
import { getNewsCategoriesTopicsIds, SubstancesTable, SelectRegulations } from "@common";

import { NewsStatusTitles, NewsStatusValues } from "../NewsUIHelpers";

import "pure-react-carousel/dist/react-carousel.es.css";

export function NewsFieldsToEdit({
  values,
  setFieldValue,
  sourceList,
  categoryList,
  regionList,
  file,
  setFile,
  coverImage,
  btnRef,
  handleSubmit,
  updateRelevantOrganizationsValues,
}) {
  useEffect(() => {
    updateRelevantOrganizationsValues({
      topics: getNewsCategoriesTopicsIds(values.news_categories),
      regulations: values.regulations,
      frameworks: values.regulatory_frameworks,
    });
  }, [values.news_categories, values.regulations, values.regulatory_frameworks]);

  const handleSelectOnChange = field => value => setFieldValue(field, value);

  const handleFileOnChange = event => {
    setFieldValue(
      "cover_image",
      event.currentTarget.files[0]
    );
    setFile(
      URL.createObjectURL(event.currentTarget.files[0])
    );
  };

  const handleFormCheck = e => setFieldValue('active', e.target.checked);

  return (
    <Form className="form form-label-right">
      <div className="form-group row">
        <div className="col-lg-12">
          <Field
            name="title"
            component={Input}
            placeholder="Title"
            label="Title *"
          />
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-12">
          <label>News Body *</label>
          <RichTextEditor
            value={values.body}
            onChange={handleSelectOnChange("body")}
          />
          <ErrorMessage name="body">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>
      </div>

      {!!values?.substances?.length && (
        <div className="row">
          <div className="col-lg-12 mb-5">
            <label>Substances</label>
            <SubstancesTable substances={values.substances}/>
          </div>
        </div>
      )}

      <div className="form-group row">
        <div className="col-lg-6">
          <DatePickerField name="pub_date" label="Publish Date *" />
          <ErrorMessage name="pub_date">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>

        <div className="col-lg-6">
          <Select name="status" label="Status *">
            {NewsStatusTitles.map((status, index) => (
              <option key={status} value={NewsStatusValues[index]}>
                {status}
              </option>
            ))}
          </Select>
          <ErrorMessage name="status">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-6">
          <label>Select Source *</label>

          <ReactSelect
            name="source"
            value={values.source}
            getOptionLabel={(option) => option.name}
            getOptionValue={(option) => option.id}
            onChange={handleSelectOnChange("source")}
            options={sourceList}
            className="basic-multi-select"
            classNamePrefix="select"
          />
          <ErrorMessage name="source">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>

        <div className="col-lg-6">
          <label>Categories *</label>
          <ReactSelect
            isMulti
            value={values.news_categories}
            getOptionLabel={(option) => `${option.name} (${option?.topic?.name || 'no topic'})`}
            getOptionValue={(option) => option.id}
            onChange={handleSelectOnChange("news_categories")}
            name="news_categories"
            options={categoryList}
            className="basic-multi-select"
            classNamePrefix="select"
          />
          <ErrorMessage name="news_categories">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>
      </div>

      <div className="form-group row">
        <SelectRegulations
          selected={values.regulations}
          onChange={handleSelectOnChange('regulations')}
          type="regulations"
          isNameTooltip
        />

        <SelectRegulations
          selected={values.regulatory_frameworks}
          onChange={handleSelectOnChange('regulatory_frameworks')}
          type="regulatory_frameworks"
          isNameTooltip
        />
      </div>

      <div className="form-group row">
        <div className="col-lg-6">
          <label>Regions</label>
          <ReactSelect
            isMulti
            value={values.regions}
            getOptionLabel={(option) => option.name}
            getOptionValue={(option) => option.id}
            onChange={handleSelectOnChange("regions")}
            name="regions"
            options={regionList}
            className="basic-multi-select"
            classNamePrefix="select"
          />
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-6">
          <div className="row">

            <div className="col-lg-12">
              <label>Select File</label>
              <input
                id="cover_image"
                name="cover_image"
                type="file"
                onChange={handleFileOnChange}
                className="form-control"
              />
            </div>

          </div>
        </div>
        <div className="col-lg-6">
          {file ? (
            <img
              className="ml-auto"
              height="150"
              width="300"
              src={file}
              alt="cover"
            />
          ) : coverImage !== "" ? (
            <img
              className="ml-auto"
              height="150"
              width="300"
              src={coverImage}
              alt="cover"
            />
          ) : null}
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-6">
          <FormCheck
            name="active"
            checked={values.active}
            type="switch"
            id="active-switch"
            label="Set active"
            onChange={handleFormCheck}
          />
        </div>
      </div>

      <button
        type="submit"
        style={{ display: "none" }}
        ref={btnRef}
        onSubmit={handleSubmit}
      />
    </Form>
  );
}
