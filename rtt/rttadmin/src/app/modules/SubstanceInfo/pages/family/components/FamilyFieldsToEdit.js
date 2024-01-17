import React from 'react';
import PropTypes from 'prop-types';
import { Form } from 'formik';

import { Search } from '@common';
import { UiKitErrorMessage } from '@common/UIKit';

const errorMessage = msg => <div style={{ marginBottom: '-20px', height: '20px', color: '#e7576c' }}>{msg}</div>;

const propTypes = {
  values: PropTypes.object.isRequired,
  setFieldValue: PropTypes.func.isRequired,
};

export const FamilyFieldsToEdit = ({ values, setFieldValue, errors }) => {
  const getOnChange = fieldName => value => setFieldValue(fieldName, value);

  return (
    <Form className="form form-label-right">
      <div className="form-group row">
        <div className="col-lg-12 position-relative">
          <label>Chemycal Id</label>

          <Search
            initialValue={values.chemycal_id}
            handleUpdateSearch={getOnChange('chemycal_id')}
            placeholder="Chemycal Id"
          />

          {errors?.chemycal_id ? errorMessage(errors.chemycal_id) : <UiKitErrorMessage name="chemycal_id" />}
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-12 position-relative">
          <label>Name</label>

          <Search initialValue={values.name} handleUpdateSearch={getOnChange('name')} placeholder="Name" />

          {errors?.name ? errorMessage(errors.name) : <UiKitErrorMessage name="name" />}
        </div>
      </div>
    </Form>
  );
};

FamilyFieldsToEdit.propTypes = propTypes;
