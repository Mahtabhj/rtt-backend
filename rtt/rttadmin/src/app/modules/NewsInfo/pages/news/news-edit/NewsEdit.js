/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import React, { useEffect, useState, useRef, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useHistory, useParams } from 'react-router-dom';
import RichTextEditor from 'react-rte';
import dayjs from 'dayjs';

import {
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  CardHeaderToolbar,
  ModalProgressBar,
} from '@metronic-partials/controls';
import { makeMaterialCategoryTree, makeProductCategoryTree } from '@metronic-helpers';
import {
  getNewsCategoriesTopicsIds,
  initialValuesForRelevantOrganization,
  useOrganizationsValues,
  useRegulationTaggedCategories,
  CheckboxBlank,
  SelectTreeView,
  VisibleToOrganization,
  NEWS,
  REVIEW,
} from '@common';
import { permissionsRoutePath } from '@common/Permissions/routesPaths';

import * as actions from '@redux-news/news/newsActions';
import * as newsApiService from '@redux-news/news/newsApiService';

import { NewsEditForm } from './NewsEditForm';
import { DocumentsTable } from '../related-documents-table/DocumentsTable';
import { ImpactAssessmentTable } from '../impact-assessment/ImpactAssessmentTable';

const initialNews = {
  id: undefined,
  title: '',
  body: RichTextEditor.createEmptyValue(),
  pub_date: dayjs().format('MM/DD/YYYY'),
  status: 'n',
  source: null,
  news_categories: [],
  regulations: [],
  regulatory_frameworks: [],
  product_categories: [],
  material_categories: [],
  regions: [],
  active: true,
  cover_image: '',
  review_yellow: false,
  review_green: false,
};

export function NewsEdit() {
  const btnRef = useRef();
  const { id } = useParams();
  const history = useHistory();
  const scrollTo = history.location.state?.scrollTo;
  const dispatch = useDispatch();
  const element = document.getElementById(REVIEW);

  const [tab, setTab] = useState('attachments');

  const {
    listLoading,
    actionsLoading,
    newsForEdit,
    sourceList,
    categoryList,
    documentList,
    regionList,
    success,
  } = useSelector(state => ({
    listLoading: state.news.listLoading,
    actionsLoading: state.news.actionsLoading,
    newsForEdit: state.news.newsForEdit,
    sourceList: state.news.sourceList,
    categoryList: state.news.categoryList,
    documentList: state.news.documentList,
    regionList: state.news.regionList,
    success: state.news.success,
  }));

  const [initNews, setInitNews] = useState(initialNews);

  const [reviewComment, setReviewComment] = useState('');

  const [productCategoriesTree, setProductCategoriesTree] = useState([]);
  const [materialCategoriesTree, setMaterialCategoriesTree] = useState([]);

  const [isTreeViewForcedUpdate, setTreeViewForcedUpdate] = useState(false);

  const [relevantOrganizationsValues, updateRelevantOrganizationsValues] = useOrganizationsValues(
    initialValuesForRelevantOrganization,
  );

  const {
    allProductChecked,
    setProductChecked,
    allMaterialChecked,
    setMaterialChecked,
    handleProductsChecked,
    handleMaterialsChecked,
    updateRegulationTaggedCategoriesCallback,
  } = useRegulationTaggedCategories(setTreeViewForcedUpdate, updateRelevantOrganizationsValues);

  const handleOnReviewCommentChange = ({ target }) => setReviewComment(target.value);

  const handleOnYellowReviewClick = useCallback(
    () =>
      setInitNews(prevState => ({
        ...prevState,
        review_yellow: !prevState.review_yellow,
      })),
    [],
  );

  const handleOnGreenReviewClick = useCallback(() => {
    setInitNews(prevState => {
      const reviewGreen = !prevState.review_green;

      dispatch(actions.updateNewsReview(id, { review_green: reviewGreen }));

      return {
        ...prevState,
        review_green: reviewGreen,
      };
    });
  }, [dispatch, id]);

  const isDropdownOptionsLoaded = !!(
    sourceList?.length &&
    categoryList?.length &&
    documentList?.length &&
    regionList?.length
  );

  useEffect(() => {
    if (scrollTo && element && newsForEdit && isDropdownOptionsLoaded && !listLoading) {
      setTimeout(() => {
        element.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
      }, 300);

      handleOnYellowReviewClick();
    }
  }, [scrollTo, element, newsForEdit, isDropdownOptionsLoaded, listLoading, handleOnYellowReviewClick]);

  useEffect(() => {
    dispatch(actions.fetchNews(id));
    dispatch(actions.fetchSourceList());
    dispatch(actions.fetchCategoryList());
    dispatch(actions.fetchOrganizationList());
    dispatch(actions.fetchDocumentList());
    dispatch(actions.fetchRegionList());
    dispatch(actions.fetchNewsRelevanceList());
  }, [id, dispatch]);

  useEffect(() => {
    newsApiService
      .getIndustries()
      .then(response => {
        const industries = response.data.results;

        const productCategoryTree = makeProductCategoryTree(industries);
        setProductCategoriesTree(productCategoryTree);

        const materialCategoryTree = makeMaterialCategoryTree(industries);
        setMaterialCategoriesTree(materialCategoryTree);
      })
      .catch(error => {
        console.error(error);
      });
  }, [dispatch]);

  useEffect(() => {
    if (newsForEdit) {
      const productCategoriesIds = newsForEdit.product_categories.map(item => item.id);
      const materialCategoriesIds = newsForEdit.material_categories.map(item => item.id);
      const regulationsIds = newsForEdit.regulations.map(item => item.id);
      const regulatoryFrameworksIds = newsForEdit.regulatory_frameworks.map(item => item.id);

      const newNewsForEdit = {
        ...newsForEdit,
        product_categories: productCategoriesIds,
        material_categories: materialCategoriesIds,
        regulations: regulationsIds,
        regulatory_frameworks: regulatoryFrameworksIds,
        body: RichTextEditor.createValueFromString(newsForEdit.body, 'html'),
        pub_date: dayjs(newsForEdit.pub_date).format('MM/DD/YYYY'),
      };
      setInitNews(newNewsForEdit);

      if (newsForEdit.review_comment) {
        setReviewComment(newsForEdit.review_comment);
      }

      setProductChecked(productCategoriesIds);
      setMaterialChecked(materialCategoriesIds);

      updateRelevantOrganizationsValues({
        product_categories: productCategoriesIds,
        material_categories: materialCategoriesIds,
        topics: getNewsCategoriesTopicsIds(newsForEdit.news_categories),
        regulations: regulationsIds,
        frameworks: regulatoryFrameworksIds,
      });
    }
  }, [newsForEdit]);

  const backToNewsList = useCallback(() => {
    history.push(permissionsRoutePath[NEWS]);
    dispatch(actions.fetchNews()); // to drop newsForEdit
  }, [dispatch, history]);

  useEffect(() => {
    if (success === 'news') {
      backToNewsList();
    }
  }, [success, backToNewsList]);

  const saveNews = values => {
    const submitValues = {
      ...values,
      body: values.body.toString('html'),
      pub_date: dayjs(values.pub_date)
        .format('YYYY-MM-DD')
        .concat('T00:00:00'),
      news_categories: values.news_categories ? values.news_categories.map(news_category => news_category.id) : [],

      product_categories: allProductChecked,
      material_categories: allMaterialChecked,

      source: values.source.id,

      documents: values.documents ? values.documents.map(document => document.id) : [],

      regions: values.regions ? values.regions.map(region => region.id) : [],

      review_comment: reviewComment || null,
    };

    if (!id) {
      dispatch(actions.createNews(submitValues));
    } else {
      delete submitValues.selected_by;
      delete submitValues.discharged_by;
      dispatch(actions.updateNews(submitValues));
    }
  };

  const dischargeNews = () => dispatch(actions.selectNewsPatch(id, { status: 'd' })).then(() => backToNewsList());

  const saveNewsClick = () => {
    if (btnRef && btnRef.current) {
      btnRef.current.click();
    }
  };

  const renderButtons = () => (
    <>
      <button type="button" onClick={backToNewsList} className="btn btn-light">
        <i className="fa fa-arrow-left" />
        Back
      </button>
      <button type="submit" className="btn btn-primary ml-2" onClick={saveNewsClick}>
        Save
      </button>
    </>
  );

  return (
    <>
      {(!id || newsForEdit) && isDropdownOptionsLoaded && !listLoading ? (
        <Card>
          {actionsLoading && <ModalProgressBar />}
          <CardHeader title={initNews.id ? `Edit News: ${initNews.title}` : 'Create News'}>
            <CardHeaderToolbar>
              {renderButtons()}
              {!!id && initNews.status !== 'd' && (
                <button type="button" className="btn btn-danger ml-2" onClick={dischargeNews}>
                  Discharge news
                </button>
              )}
            </CardHeaderToolbar>
          </CardHeader>
          <CardBody>
            <NewsEditForm
              actionsLoading={actionsLoading}
              news={initNews}
              btnRef={btnRef}
              saveNews={saveNews}
              sourceList={sourceList}
              categoryList={categoryList}
              documentList={documentList}
              regionList={regionList}
              productCategories={allProductChecked}
              materialCategories={allMaterialChecked}
              updateRelevantOrganizationsValues={updateRelevantOrganizationsValues}
              updateRegulationTaggedCategoriesCallback={updateRegulationTaggedCategoriesCallback}
            />

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
          </CardBody>
        </Card>
      ) : (
        <ModalProgressBar />
      )}

      {id && newsForEdit && (
        <Card>
          <CardBody>
            <ul className="nav nav-tabs nav-tabs-line " role="tablist">
              <li className="nav-item" onClick={() => setTab('attachments')}>
                <a
                  className={`nav-link ${tab === 'attachments' && 'active'}`}
                  data-toggle="tab"
                  role="button"
                  aria-selected={(tab === 'attachments').toString()}
                >
                  Attachments
                </a>
              </li>

              <li className="nav-item" onClick={() => setTab('impact-assessment')}>
                <a
                  className={`nav-link ${tab === 'impact-assessment' && 'active'}`}
                  data-toggle="tab"
                  role="button"
                  aria-selected={(tab === 'impact-assessment').toString()}
                >
                  Impact Assessment
                </a>
              </li>
            </ul>
            <div className="mt-5">
              {tab === 'attachments' && id && <DocumentsTable newsId={+id} />}

              {tab === 'impact-assessment' && id && (
                <ImpactAssessmentTable newsId={+id} newsTitle={newsForEdit?.title} />
              )}
            </div>
          </CardBody>
        </Card>
      )}

      {!!id && ((initNews.active && initNews.status === 's') || initNews.status === 'd') && (
        <Card>
          <CardHeader title="Review">
            <CardHeaderToolbar>
              <CheckboxBlank
                className="mr-3"
                isSelected={initNews.review_yellow}
                onClick={handleOnYellowReviewClick}
                type="yellow"
              />
              <CheckboxBlank isSelected={initNews.review_green} onClick={handleOnGreenReviewClick} type="green" />
            </CardHeaderToolbar>
          </CardHeader>

          <CardBody>
            <textarea className="form-control" value={reviewComment} onChange={handleOnReviewCommentChange} rows={5} />
          </CardBody>

          <CardFooter>
            <div className="d-flex justify-content-end">{renderButtons()}</div>
          </CardFooter>

          <div id={REVIEW} />
        </Card>
      )}
    </>
  );
}
