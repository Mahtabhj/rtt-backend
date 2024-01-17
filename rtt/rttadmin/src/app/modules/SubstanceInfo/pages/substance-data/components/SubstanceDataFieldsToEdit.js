import React, { useEffect, useRef } from 'react';
import { useSelector } from 'react-redux';
import ReactSelect from 'react-select';
import PropTypes from 'prop-types';
import { Form } from 'formik';

import { SelectSubstance } from '@common';
import { UiKitErrorMessage } from '@common/UIKit';

import { propertyListSelector } from '../../../_redux/substance-data/substanceDataSelectors';

import { PropertyDataPoints } from './PropertyDataPoints/PropertyDataPoints';

const prepareEmptyPropertyDataPoint = ({ id, name }) => ({
  id,
  name,
  value: '',
  status: 'active',
  modified: '',
  image: null,
  isChecked: false,
});

const propTypes = {
  values: PropTypes.object.isRequired,
  setFieldValue: PropTypes.func.isRequired,
  isEdit: PropTypes.bool.isRequired,
};

export const SubstanceDataFieldsToEdit = ({ values, setFieldValue, isEdit }) => {
  const isInitialized = useRef(false);

  const propertyList = useSelector(propertyListSelector);

  useEffect(() => {
    const editingDataPoints = values.property_data_points;

    if (isEdit && !isInitialized.current && editingDataPoints?.length) {
      setFieldValue(
        'property_data_points',
        editingDataPoints.map(dataPoint =>
          dataPoint.editPointId ? dataPoint : prepareEmptyPropertyDataPoint(dataPoint),
        ),
      );

      isInitialized.current = true;
    }
  }, [values, setFieldValue, isEdit, propertyList]);

  const handleOnChangeSubstance = value => setFieldValue('substance', value);
  const handleOnChangeProperty = ({ property_data_points, ...value }) => {
    setFieldValue('property', value);
    setFieldValue('property_data_points', property_data_points.map(prepareEmptyPropertyDataPoint));
  };
  const handleOnChangePropertyDataPoints = value => setFieldValue('property_data_points', value);

  return (
    <>
      <Form className="form form-label-right">
        <div className="form-group row">
          {/* Substance */}
          <SelectSubstance selected={values.substance} onChange={handleOnChangeSubstance} isDisabled={isEdit}>
            <UiKitErrorMessage name="substance" />
          </SelectSubstance>

          {/* Property */}
          <div className="col-lg-6">
            <label>Property</label>

            <ReactSelect
              name="property"
              value={values.property}
              getOptionLabel={({ name }) => name}
              getOptionValue={({ id }) => id}
              onChange={handleOnChangeProperty}
              options={propertyList}
              isDisabled={isEdit}
              className="basic-multi-select"
              classNamePrefix="select"
            />
            <UiKitErrorMessage name="property" />
          </div>
        </div>
      </Form>

      <label>Property data point</label>
      <PropertyDataPoints values={values.property_data_points} updateCallback={handleOnChangePropertyDataPoints} />
    </>
  );
};

SubstanceDataFieldsToEdit.propTypes = propTypes;
