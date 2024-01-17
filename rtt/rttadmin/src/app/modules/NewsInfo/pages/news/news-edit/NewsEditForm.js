import React, { useState } from 'react';
import { Formik } from 'formik';
import * as Yup from 'yup';

import { RegulationTaggedCategories } from '@common';

import { NewsFieldsToEdit } from './NewsFieldsToEdit';

// Validation schema
const NewsEditSchema = Yup.object().shape({
  title: Yup.string()
    .ensure()
    .required('Title is required'),
  status: Yup.string()
    .ensure()
    .required('Status is required'),
  pub_date: Yup.string()
    .ensure()
    .required('Publish date is required'),
  source: Yup.string()
    .ensure()
    .required('Source is required'),
  news_categories: Yup.string()
    .ensure()
    .required('Categories is required'),
});

export function NewsEditForm({
  news,
  btnRef,
  saveNews,
  sourceList,
  categoryList,
  regionList,
  productCategories,
  materialCategories,
  updateRelevantOrganizationsValues,
  updateRegulationTaggedCategoriesCallback,
}) {
  const [file, setFile] = useState(null);

  const handleOnSubmit = values => saveNews(values);

  return (
    <Formik enableReinitialize initialValues={news} validationSchema={NewsEditSchema} onSubmit={handleOnSubmit}>
      {({ values, setFieldValue, handleSubmit }) => (
        <>
          <RegulationTaggedCategories
            regulations={values.regulations}
            frameworks={values.regulatory_frameworks}
            productCategories={productCategories}
            materialCategories={materialCategories}
            updateCategoriesCallback={updateRegulationTaggedCategoriesCallback}
          />

          <NewsFieldsToEdit
            values={values}
            setFieldValue={setFieldValue}
            sourceList={sourceList}
            categoryList={categoryList}
            regionList={regionList}
            file={file}
            setFile={setFile}
            coverImage={news.cover_image}
            btnRef={btnRef}
            handleSubmit={handleSubmit}
            updateRelevantOrganizationsValues={updateRelevantOrganizationsValues}
          />
        </>
      )}
    </Formik>
  );
}
