import React from 'react';
import ReactSelect from 'react-select';
import RichTextEditor from 'react-rte';
import { Form, Field, ErrorMessage } from 'formik';

import { Input, Select } from '@metronic-partials/controls';

const reviewStatusList = [
  { id: 1, name: 'Online', value: 'o' },
  { id: 2, name: 'Draft', value: 'd' },
];

const getOptionLabel = ({ name }) => name;
const getOptionValue = ({ id }) => id;

const RegulationFieldsToEdit = ({
  values,
  setFieldValue,
  handleSubmit,
  updateRelevantOrganizationsValues,
  btnRef,
  statusList,
  regulatoryFrameworkList,
  languageList,
  regulationTypeList,
  topicList,
  getCategoriesCallback,
}) => {
  const getHandleOnChange = fieldName => value => {
    setFieldValue(fieldName, value);

    if (fieldName === 'regulatory_framework') {
      // RTT-1028 update categories tree on RF select when creating new R

      if (getCategoriesCallback) {
        const { product_categories, material_categories, name } = value;
        const productCategoriesIds = product_categories.map(({ id }) => id);
        const materialCategoriesIds = material_categories.map(({ id }) => id);

        getCategoriesCallback({
          product_categories: productCategoriesIds,
          material_categories: materialCategoriesIds,
          taggedName: name,
        });
      }
    }

    if (fieldName === 'topics') {
      const topicIds = (value || []).map(({ id }) => id);

      updateRelevantOrganizationsValues({ topics: topicIds });
    }
  };

  return (
    <Form className="form form-label-right">
      <div className="form-group mb-2 row">
        <div className="col-lg-6">
          <Field name="name" component={Input} withFeedbackLabel={false} placeholder="Name" label="Name *" />
          <ErrorMessage name="name">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>

        <div className="col-lg-6 mb-2 form-group">
          <label>Regulation Type *</label>
          <Field
            name="type"
            component={() => (
              <ReactSelect
                isMulti={false}
                options={regulationTypeList}
                getOptionLabel={getOptionLabel}
                getOptionValue={getOptionValue}
                value={values.type}
                onChange={getHandleOnChange('type')}
              />
            )}
          />
          <ErrorMessage name="type">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>
      </div>

      <div className="form-group mb-2 row">
        <div className="col-lg-6 mb-2 form-group">
          <label>Status List *</label>
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

        {/* Review Status */}
        <div className="col-lg-6">
          <Select name="review_status" label="Review Status *">
            {reviewStatusList.map(source => (
              <option key={source.id} value={source.value}>
                {source.name}
              </option>
            ))}
          </Select>
          <ErrorMessage name="review_status">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>
      </div>

      <div className="form-group mb-2 row">
        <div className="col-lg-6 mb-2 form-group">
          <label>Regulatory Framework *</label>
          <Field
            name="regulatory_framework"
            component={() => (
              <ReactSelect
                isMulti={false}
                options={regulatoryFrameworkList}
                getOptionLabel={getOptionLabel}
                getOptionValue={getOptionValue}
                value={values.regulatory_framework}
                onChange={getHandleOnChange('regulatory_framework')}
              />
            )}
          />
          <ErrorMessage name="regulatory_framework">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>

        <div className="col-lg-6 mb-2 form-group">
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
      </div>

      <div className="row form-group">
        <div className="col-lg-6">
          <label>Topics</label>
          <ReactSelect
            isMulti
            value={values.topics}
            getOptionLabel={getOptionLabel}
            getOptionValue={getOptionValue}
            onChange={getHandleOnChange('topics')}
            name="topics"
            options={topicList}
            className="basic-multi-select"
            classNamePrefix="select"
          />
          <ErrorMessage name="topics">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>
      </div>

      <div className="form-group mb-2 row position-relative zindex-0">
        <div className="col-lg-12">
          <label>Description</label>

          <RichTextEditor value={values.description} onChange={getHandleOnChange('description')} />

          <ErrorMessage name="description">{msg => <div style={{ color: 'red' }}>{msg}</div>}</ErrorMessage>
        </div>
      </div>

      <button type="submit" style={{ display: 'none' }} ref={btnRef} onSubmit={handleSubmit} />
    </Form>
  );
};

export default RegulationFieldsToEdit;
