import React from 'react';
import { Formik } from 'formik';
import * as Yup from 'yup';

import RegulationFieldsToEdit from './RegulationFieldsToEdit';

// Validation schema
const RegulationEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(1, 'Minimum 1 character')
    .max(200, 'Maximum 200 characters')
    .required('Name is required'),
  type: Yup.string()
    .ensure()
    .required('Regulation type is required'),
  status: Yup.string()
    .ensure()
    .required('Status is required'),
  regulatory_framework: Yup.string()
    .ensure()
    .required('Regulatory framework is required'),
  language: Yup.string()
    .ensure()
    .required('Language is required'),
});

const RegulationEditForm = ({
  regulation,
  updateRelevantOrganizationsValues,
  btnRef,
  saveRegulation,
  statusList,
  regulatoryFrameworkList,
  languageList,
  regulationTypeList,
  topicList,
  getRegulationTaggedCategoriesCallback,
}) => (
  <Formik
    enableReinitialize
    initialValues={regulation}
    validationSchema={RegulationEditSchema}
    onSubmit={saveRegulation}
  >
    {({ handleSubmit, setFieldValue, values }) => (
      <RegulationFieldsToEdit
        values={values}
        setFieldValue={setFieldValue}
        handleSubmit={handleSubmit}
        updateRelevantOrganizationsValues={updateRelevantOrganizationsValues}
        btnRef={btnRef}
        statusList={statusList}
        regulatoryFrameworkList={regulatoryFrameworkList}
        languageList={languageList}
        regulationTypeList={regulationTypeList}
        topicList={topicList}
        getCategoriesCallback={getRegulationTaggedCategoriesCallback}
      />
    )}
  </Formik>
);

export default RegulationEditForm;
