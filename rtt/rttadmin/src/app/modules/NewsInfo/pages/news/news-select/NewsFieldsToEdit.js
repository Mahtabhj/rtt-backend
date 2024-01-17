import React, { useEffect } from "react";
import ReactSelect from "react-select";
import { FormCheck } from 'react-bootstrap';
import { Form, Field, ErrorMessage } from "formik";

import { Input, DatePickerField } from "@metronic-partials/controls";

import { getNewsCategoriesTopicsIds, SelectRegulations } from "@common";

import "pure-react-carousel/dist/react-carousel.es.css";

export function NewsFieldsToEdit({
  sourceList,
  categoryList,
  regionList,
  setFieldValue,
  values,
  disabled,
  updateRelevantOrganizationsValues,
}) {
  useEffect(() => {
    if (values.id) {
      updateRelevantOrganizationsValues({
        topics: getNewsCategoriesTopicsIds(values.news_categories),
        regulations: values.regulations,
        frameworks: values.regulatory_frameworks,
      });
    }
  }, [values.id, values.news_categories, values.regulations, values.regulatory_frameworks]);

  const handleSelectOnChange = field => value => setFieldValue(field, value);

  const handleFormCheck = e => setFieldValue('active', e.target.checked);

  return (
    <Form className="form form-label-right">
      <div className="form-group row">
        <div className="col-lg-12">
          <Field
            disabled={disabled}
            name="title"
            component={Input}
            placeholder="Title"
            label="Title *"
          />
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-6">
          <DatePickerField name="pub_date" label="Publish Date *" disabled={disabled} />

          <ErrorMessage name="pub_date">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>

        <div className="col-lg-6">
          <label>Select Source *</label>

          <ReactSelect
            name="source"
            value={values.source}
            getOptionLabel={(option) => option.name}
            getOptionValue={(option) => option.id}
            onChange={handleSelectOnChange("source")}
            options={sourceList}
          />
          <ErrorMessage name="source">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>
      </div>

      <div className="form-group row">
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
            disabled={disabled}
          />

          <ErrorMessage name="news_categories">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>

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
            disabled={disabled}
          />
        </div>
      </div>

      <div className="form-group row">
        <SelectRegulations
          selected={values.regulations}
          onChange={handleSelectOnChange('regulations')}
          type="regulations"
          isDisabled={disabled}
          isNameTooltip
        />

        <SelectRegulations
          selected={values.regulatory_frameworks}
          onChange={handleSelectOnChange('regulatory_frameworks')}
          type="regulatory_frameworks"
          isDisabled={disabled}
          isNameTooltip
        />
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
            disabled={disabled}
          />
        </div>
      </div>
    </Form>
  );
}
