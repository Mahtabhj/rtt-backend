import React from 'react';
import ReactSelect from 'react-select';
import RichTextEditor from 'react-rte';
import { Form, Field, ErrorMessage } from 'formik';

import { Input, Select } from '@metronic-partials/controls';
import { SelectIssuingBody } from '@common/SelectIssuingBody/SelectIssuingBody';

const RegulatoryFrameworkFieldsToEdit = ({
  values,
  setFieldValue,
  handleSubmit,
  updateRelevantOrganizationsValues,
  btnRef,
  languageList,
  statusList,
  regionList,
  topicList,
}) => {
  const getOptionLabel = ({ name }) => name;
  const getOptionValue = ({ id }) => id;
  const getHandleOnChange = fieldName => value => {
    setFieldValue(fieldName, fieldName === 'issuing_body' ? value.id : value);

    if (fieldName === 'topics') {
      const topicIds = (value || []).map(({ id }) => id);

      updateRelevantOrganizationsValues({ topics: topicIds });
    }
  };
  const handleOnSubmit = () => handleSubmit();

  return (
    <Form className="form form-label-right">
      <div className="form-group row mb-2">
        <div className="col-lg-6">
          <Field name="name" component={Input} placeholder="Name" label="Name *" withFeedbackLabel={false} />
        </div>

        <div className="col-lg-6">
          <Select name="review_status" label="Review Status *" withFeedbackLabel={false}>
            <option key="true" value="d">
              Draft
            </option>
            <option key="false" value="o">
              Online
            </option>
          </Select>
          <ErrorMessage name="review_status">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>
      </div>
      <div className="row form-group">
        <div className="col-lg-6">
          <label>Language *</label>
          <Field
            name="language"
            component={() => (
              <ReactSelect
                isMulti={false}
                options={languageList}
                getOptionLabel={getOptionLabel}
                getOptionValue={getOptionValue}
                value={values.language}
                onChange={getHandleOnChange('language')}
              />
            )}
          />
          <ErrorMessage name="language">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>

        <div className="col-lg-6">
          <label>Status *</label>
          <Field
            name="status"
            component={() => (
              <ReactSelect
                isMulti={false}
                options={statusList}
                getOptionLabel={getOptionLabel}
                getOptionValue={getOptionValue}
                value={values.status}
                onChange={getHandleOnChange('status')}
              />
            )}
          />
          <ErrorMessage name="status">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>
      </div>

      <div className="row form-group">
        <SelectIssuingBody selectedId={values.issuing_body} onChange={getHandleOnChange('issuing_body')} />

        <div className="col-lg-6">
          <label>Regions *</label>
          <ReactSelect
            name="regions"
            isMulti
            value={values.regions}
            getOptionLabel={getOptionLabel}
            getOptionValue={getOptionValue}
            onChange={getHandleOnChange('regions')}
            options={regionList}
            className="basic-multi-select"
            classNamePrefix="select"
          />
          <ErrorMessage name="regions">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>
      </div>

      <div className="row form-group">
        <div className="col-lg-6">
          <label>Topics</label>
          <ReactSelect
            name="topics"
            isMulti
            value={values.topics}
            getOptionLabel={getOptionLabel}
            getOptionValue={getOptionValue}
            onChange={getHandleOnChange('topics')}
            options={topicList}
            className="basic-multi-select"
            classNamePrefix="select"
          />
          <ErrorMessage name="topics">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>
      </div>

      <div className="form-group row position-relative zindex-0">
        <div className="col-lg-12 mb-3">
          <label>Description</label>

          <RichTextEditor value={values.description} onChange={getHandleOnChange('description')} />

          <ErrorMessage name="description">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>
      </div>
      <button type="submit" style={{ display: 'none' }} ref={btnRef} onSubmit={handleOnSubmit} />
    </Form>
  );
};

export default RegulatoryFrameworkFieldsToEdit;
