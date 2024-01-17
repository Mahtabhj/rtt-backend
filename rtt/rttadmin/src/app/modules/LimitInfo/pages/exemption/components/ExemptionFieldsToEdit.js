import React from "react";
import ReactSelect from "react-select";
import PropTypes from "prop-types";
import { ErrorMessage, Field, Form } from "formik";

import { Input } from "@metronic-partials/controls";

import { DateInput, SelectRegulations, SelectSubstance, statusOptions } from "@common";

const propTypes = {
  values: PropTypes.object.isRequired,
  setFieldValue: PropTypes.func.isRequired,
}

export const ExemptionFieldsToEdit = ({ values, setFieldValue }) => {
  const handleOnChangeRegulation = value => {
    setFieldValue('regulatory_framework', '');
    setFieldValue('regulation', `${value}`);
  };

  const handleOnChangeRegulatoryFramework = value => {
    setFieldValue('regulation', '');
    setFieldValue('regulatory_framework', `${value}`);
  };

  const handleOnChangeSubstance = value => setFieldValue('substance', value);
  const handleOnChangeApplication = value => setFieldValue('scope', value);
  const handleOnChangeStatus = status => setFieldValue('status', status.value);
  const handleOnChangeDate = ({ id, value }) => setFieldValue(id, value ? value.toISOString() : '');

  return (
    <Form className="form form-label-right">
      <div className="form-group row">
        {/* Regulation */}
        <SelectRegulations
          selected={values.regulation ? +values.regulation : null}
          onChange={handleOnChangeRegulation}
          type="regulations"
          isSingle
        >
          <ErrorMessage name="regulation">
            {(msg) => <div style={{ color: "#e7576c" }}>{msg}</div>}
          </ErrorMessage>
        </SelectRegulations>

        {/* Regulatory framework */}
        <SelectRegulations
          selected={values.regulatory_framework ? +values.regulatory_framework : null}
          onChange={handleOnChangeRegulatoryFramework}
          type="regulatory_frameworks"
          isSingle
        >
          <ErrorMessage name="regulatory_framework">
            {(msg) => <div style={{ color: "#e7576c" }}>{msg}</div>}
          </ErrorMessage>
        </SelectRegulations>
      </div>

      <div className="form-group row">
        {/* Substance */}
        <SelectSubstance
          selected={values.substance}
          onChange={handleOnChangeSubstance}
        >
          <ErrorMessage name="substance">
            {(msg) => <div style={{ color: "#e7576c" }}>{msg}</div>}
          </ErrorMessage>
        </SelectSubstance>
      </div>

      <div className="form-group row">
        <div className="col-lg-3">
          <Field
            label="Article/Annex"
            name="article"
            component={Input}
          />
        </div>

        <div className="col-lg-3">
          <Field
            label="Reference"
            name="reference"
            component={Input}
          />
        </div>
      </div>

      <div className="form-group row">
        {/* Application */}
        <div className="col-lg-12">
          <label>Application</label>
          <Field
            className="form-control"
            name="application"
            as="textarea"
            rows={3}
          />
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-3">
          <label>Expiration date</label>
          <DateInput
            id="expiration_date"
            value={values.expiration_date}
            onChangeCallback={handleOnChangeDate}
          />
        </div>

        <div className="col-lg-3">
          <label>Date into force</label>
          <DateInput
            id="date_into_force"
            value={values.date_into_force}
            onChangeCallback={handleOnChangeDate}
          />
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-6">
          <label>Status</label>
          <ReactSelect
            value={statusOptions.find(option => option.value === values.status)}
            getOptionLabel={option => option.title}
            getOptionValue={option => option.value}
            onChange={handleOnChangeStatus}
            name="status"
            options={statusOptions}
          />

          <ErrorMessage name="status">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>

        <div className="col-lg-3">
          <label>Updated on</label>
          <DateInput
            id="modified"
            value={values.modified}
            onChangeCallback={handleOnChangeDate}
          />

          <ErrorMessage name="modified">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>
      </div>
    </Form>
  )
}

ExemptionFieldsToEdit.propTypes = propTypes;
