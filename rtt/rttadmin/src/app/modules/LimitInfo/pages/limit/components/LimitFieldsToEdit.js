import React, { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import ReactSelect from "react-select";
import PropTypes from "prop-types";
import { ErrorMessage, Field, Form } from "formik";

import { getLimitAttributes } from "../../../_redux/limit/limitActions";
import { limitAttributesSelector } from "../../../_redux/limit/limitSelectors";

import { Input } from "@metronic-partials/controls";

import { DateInput, SelectRegulations, SelectSubstance, statusOptions } from "@common";

import { SelectAttributes } from "@common/SelectAttributes/SelectAttributes";

const propTypes = {
  values: PropTypes.object.isRequired,
  setFieldValue: PropTypes.func.isRequired,
  isFullForm: PropTypes.bool.isRequired,
}

export const LimitFieldsToEdit = ({ values, setFieldValue, isFullForm }) => {
  const dispatch = useDispatch();

  const [additionalAttributeValues, setAdditionalAttributeValues] = useState([]);

  const attributes = useSelector(limitAttributesSelector);

  const fetchAttributes = useCallback((id, isRegulation) => {
    dispatch(getLimitAttributes({
      regulation_id: id,
      is_regulation: isRegulation
    }));
  }, [dispatch]);

  useEffect(() => {
    if (values.regulation) {
      fetchAttributes(values.regulation, true);
    }

    if (values.regulatory_framework) {
      fetchAttributes(values.regulatory_framework, false);
    }
  }, [values.regulation, values.regulatory_framework, fetchAttributes]);

  useEffect(() => {
    if (!additionalAttributeValues.length && values.additional_attribute_values.length) {
      setAdditionalAttributeValues(values.additional_attribute_values);
    }
  }, [additionalAttributeValues.length, values.additional_attribute_values]);

  const handleOnChangeRegulation = value => {
    fetchAttributes(value, true);
    setFieldValue('regulatory_framework', '');
    setFieldValue('regulation', `${value}`);
  };

  const handleOnChangeRegulatoryFramework = value => {
    fetchAttributes(value, false);
    setFieldValue('regulation', '');
    setFieldValue('regulatory_framework', `${value}`);
  };

  const handleOnChangeSubstance = value => setFieldValue('substance', value);
  const handleOnChangeAttributes = attributeValues => setFieldValue('additional_attribute_values', attributeValues);
  const handleOnChangeStatus = status => setFieldValue('status', status.value);

  const handleOnChangeDate = ({ id, value }) => setFieldValue(id, value ? value.toISOString() : '');

  return (
    <Form className="form form-label-right">
      {isFullForm && (
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
      )}

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
        {/* Scope */}
        <div className="col-lg-12">
          <label>Scope</label>
          <Field
            className="form-control"
            name="scope"
            as="textarea"
            rows={3}
          />

          <ErrorMessage name="scope">
            {(msg) => <div style={{ color: "#e7576c" }}>{msg}</div>}
          </ErrorMessage>
        </div>
      </div>

      <div className="form-group row">
        {/* Limit */}
        <div className="col-lg-3">
          <Field
            name="limit_value"
            label="Limit value"
            component={Input}
          />
        </div>

        <div className="col-lg-3">
          <Field
            label="Limit UoM"
            name="measurement_limit_unit"
            component={Input}
          />

          <ErrorMessage name="measurement_limit_unit">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>
      </div>

      <div className="form-group row">
        {/* Limit note */}
        <div className="col-lg-12">
          <label>Limit note</label>
          <Field
            className="form-control"
            name="limit_note"
            as="textarea"
            rows={3}
          />

          <ErrorMessage name="limit_note">
            {(msg) => <div style={{ color: "#e7576c" }}>{msg}</div>}
          </ErrorMessage>
        </div>
      </div>

      {isFullForm && (
        <div className="form-group row">
          <div className="col-lg-9">
            <label>Attributes</label>
            <SelectAttributes
              values={additionalAttributeValues}
              attributes={attributes}
              updateCallback={handleOnChangeAttributes}
            />

            <ErrorMessage name="additional_attribute_values">
              {(msg) => <div style={{ color: "red" }}>{msg}</div>}
            </ErrorMessage>
          </div>
        </div>
      )}

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
          <label>Date into force</label>
          <DateInput
            id="date_into_force"
            value={values.date_into_force}
            onChangeCallback={handleOnChangeDate}
          />

          <ErrorMessage name="date_into_force">
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

LimitFieldsToEdit.propTypes = propTypes;
