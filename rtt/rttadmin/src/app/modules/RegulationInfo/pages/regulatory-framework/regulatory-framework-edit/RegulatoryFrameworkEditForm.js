import React from 'react';
import { Formik } from 'formik';
import * as Yup from 'yup';

import RegulatoryFrameworkFieldsToEdit from './RegulatoryFrameworkFieldsToEdit';

// Validation schema
const RegulatoryFrameworkEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, 'Minimum 2 symbols')
    .max(150, 'Maximum 150 symbols')
    .required('Name is required'),
  review_status: Yup.string()
    .ensure()
    .required('Review status is required'),
  language: Yup.string()
    .ensure()
    .required('Language is required'),
  status: Yup.string()
    .ensure()
    .required('Status is required'),
  issuing_body: Yup.string()
    .ensure()
    .required('Issuing body is required'),
  regions: Yup.string()
    .ensure()
    .required('Regions is required'),
});

const RegulatoryFrameworkEditForm = ({
  regulatoryFramework,
  updateRelevantOrganizationsValues,
  btnRef,
  saveRegulatoryFramework,
  languageList,
  statusList,
  regionList,
  topicList,
}) => (
  <Formik
    enableReinitialize
    initialValues={regulatoryFramework}
    validationSchema={RegulatoryFrameworkEditSchema}
    onSubmit={values => saveRegulatoryFramework(values)}
  >
    {formikProps => (
      <RegulatoryFrameworkFieldsToEdit
        {...formikProps}
        updateRelevantOrganizationsValues={updateRelevantOrganizationsValues}
        btnRef={btnRef}
        languageList={languageList}
        statusList={statusList}
        regionList={regionList}
        topicList={topicList}
      />
    )}
  </Formik>
);

export default RegulatoryFrameworkEditForm;
