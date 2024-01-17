import React, { useEffect } from 'react';
import { Form, Formik, useFormikContext } from 'formik';
import ReactSelect from 'react-select';
import PropTypes from 'prop-types';

import { Checkbox } from '@metronic-partials/controls';

import { DateInput, Search, statusOptions } from '@common';
import { UiKitErrorMessage } from '@common/UIKit';

const getFileNameFromUrl = imageUrl => {
  const fileName = imageUrl ? imageUrl.substring(imageUrl.lastIndexOf('/') + 1).split('?')[0] : '';

  return `${fileName.slice(0, 13)} ... ${fileName.slice(-12)}`;
};

const validate = values => {
  const errors = {};

  if (values.isChecked) {
    if (!values.value) {
      errors.value = 'Value is required';
    }
  }

  return errors;
};

const AutoSubmitChecked = () => {
  const { values, submitForm } = useFormikContext();

  useEffect(() => {
    if (values.isChecked) submitForm().then(() => {});
  }, [values, submitForm]);

  return null;
};

const propTypes = {
  item: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string,
    value: PropTypes.string,
    status: PropTypes.oneOf(['active', 'deleted']),
    modified: PropTypes.string,
    image: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
    isChecked: PropTypes.bool,
  }).isRequired,
  updateItemCallback: PropTypes.func.isRequired,
};

export const DataPointItem = ({ item, updateItemCallback }) => {
  const handleOnCheckboxSelect = () => updateItemCallback({ ...item, isChecked: !item.isChecked });
  const handleOnInputChange = value => updateItemCallback({ ...item, value });
  const handleOnFileChange = ({ currentTarget }) => updateItemCallback({ ...item, image: currentTarget.files[0] });
  const handleOnChangeStatus = status => updateItemCallback({ ...item, status: status.value });
  const handleOnChangeDate = ({ value }) => updateItemCallback({ ...item, modified: value ? value.toISOString() : '' });

  return (
    <Formik
      enableReinitialize
      initialValues={item}
      validate={validate}
      onSubmit={(_, actions) => actions.setSubmitting(false)}
    >
      {({ values }) => (
        <Form className="form form-label-right">
          <div className="form-group row">
            <div className="col-lg-6 d-flex align-items-center">
              <Checkbox isSelected={!!values.isChecked} onChange={handleOnCheckboxSelect} />
              <span className="ml-3">{values.name}</span>
            </div>

            <div className="col-lg-6 position-relative">
              <Search initialValue={values.value} handleUpdateSearch={handleOnInputChange} placeholder="Value" />

              <UiKitErrorMessage name="value" />
            </div>
          </div>
          <div className="form-group row">
            <div className="col-lg-6">
              <label>Image</label>
              <div className="position-relative d-flex align-items-center">
                <input
                  className="d-flex mt-2 mb-2"
                  style={typeof values.image === 'string' ? { color: 'transparent' } : null}
                  name="image"
                  type="file"
                  onChange={handleOnFileChange}
                  id="image"
                />
                {typeof values.image === 'string' && (
                  <span className="position-absolute" style={{ left: '95px' }}>
                    {getFileNameFromUrl(values.image)}
                  </span>
                )}
              </div>

              <UiKitErrorMessage name="image" />
            </div>

            <div className="col-lg-3">
              <label>Status</label>
              <ReactSelect
                name="status"
                options={statusOptions}
                value={statusOptions.find(({ value }) => value === values.status)}
                getOptionLabel={({ title }) => title}
                getOptionValue={({ value }) => value}
                onChange={handleOnChangeStatus}
              />
            </div>

            <div className="col-lg-3">
              <label>Updated on</label>
              <DateInput id="modified" value={values.modified} onChangeCallback={handleOnChangeDate} />
            </div>
          </div>

          <AutoSubmitChecked />
        </Form>
      )}
    </Formik>
  );
};

DataPointItem.propTypes = propTypes;
