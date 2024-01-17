import React, { useEffect, useState } from 'react';
import Spinner from 'react-bootstrap/Spinner';
import * as Yup from 'yup';
import { Formik } from 'formik';

import { NEWS, RegulationTaggedCategories, SelectTreeView, VisibleToOrganization, useRegulationTaggedCategories } from '@common';

import { NewsDocsForm } from './NewsDocsForm';
import { NewsFieldsToEdit } from './NewsFieldsToEdit';

import 'pure-react-carousel/dist/react-carousel.es.css';

const schema = Yup.object().shape({
  title: Yup.string()
    .ensure()
    .required('Title is required'),
  pub_date: Yup.string()
    .ensure()
    .required('Publish date is required'),
  news_categories: Yup.string()
    .ensure()
    .required('Categories is required'),
  source: Yup.string()
    .ensure()
    .required('Source is required'),
});

export function NewsSelectForm({
  news,
  saveNews,
  newsDocs,
  newsDocTypes,
  productCategoriesTree,
  materialCategoriesTree,
  categoryList,
  regionList,
  sourceList,
  isSubmitting,
  relevantOrganizationsValues,
  updateRelevantOrganizationsValues,
}) {
  const [isTreeViewForcedUpdate, setTreeViewForcedUpdate] = useState(false);

  const {
    allProductChecked,
    setProductChecked,
    allMaterialChecked,
    setMaterialChecked,
    handleProductsChecked,
    handleMaterialsChecked,
    updateRegulationTaggedCategoriesCallback,
  } = useRegulationTaggedCategories(setTreeViewForcedUpdate, updateRelevantOrganizationsValues);

  useEffect(() => {
    setProductChecked(news.product_categories);
    setMaterialChecked(news.material_categories);
  }, []);

  const handleOnSubmit = values =>
    saveNews(
      { ...values, productChecked: allProductChecked, materialChecked: allMaterialChecked },
      'finish news selection',
    );

  const handleOnDischarge = () => saveNews(null, 'discharge');

  return (
    news && (
      <Formik enableReinitialize initialValues={news} validationSchema={schema} onSubmit={handleOnSubmit}>
        {({ handleSubmit, setFieldValue, values }) => (
          <>
            <RegulationTaggedCategories
              regulations={values.regulations}
              frameworks={values.regulatory_frameworks}
              productCategories={allProductChecked}
              materialCategories={allMaterialChecked}
              updateCategoriesCallback={updateRegulationTaggedCategoriesCallback}
            />

            <NewsFieldsToEdit
              className="d-block w-100"
              setFieldValue={setFieldValue}
              values={values}
              categoryList={categoryList}
              regionList={regionList}
              sourceList={sourceList}
              disabled={isSubmitting}
              updateRelevantOrganizationsValues={updateRelevantOrganizationsValues}
            />

            {!!newsDocs?.length && (
              <NewsDocsForm newsId={values.id} newsDocs={newsDocs} newsDocTypes={newsDocTypes} saveNews={saveNews} />
            )}

            <SelectTreeView
              productCategoriesTree={productCategoriesTree}
              productChecked={allProductChecked}
              setProductChecked={handleProductsChecked}
              materialCategoriesTree={materialCategoriesTree}
              materialChecked={allMaterialChecked}
              setMaterialChecked={handleMaterialsChecked}
              isForcedUpdate={isTreeViewForcedUpdate}
            />

            <VisibleToOrganization type={NEWS} valuesForRelevantOrganizations={relevantOrganizationsValues} />

            <div className="form-group row">
              <div className="d-flex col-lg-12 justify-content-between">
                <button
                  disabled={isSubmitting}
                  type="button"
                  onClick={handleSubmit}
                  className="btn btn-primary "
                  style={{ width: '165px' }}
                >
                  {isSubmitting ? (
                    <Spinner as="span" animation="grow" size="sm" role="status" aria-hidden="true" />
                  ) : (
                    'Finish news selection'
                  )}
                </button>

                <button
                  disabled={isSubmitting}
                  type="button"
                  onClick={handleOnDischarge}
                  className="btn btn-danger"
                  style={{ width: '165px' }}
                >
                  {isSubmitting ? (
                    <Spinner as="span" animation="grow" size="sm" role="status" aria-hidden="true" />
                  ) : (
                    'Discharge news'
                  )}
                </button>
              </div>
            </div>
          </>
        )}
      </Formik>
    )
  );
}
