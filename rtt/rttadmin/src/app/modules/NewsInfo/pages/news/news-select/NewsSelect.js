import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useHistory, useParams } from 'react-router-dom';
import dayjs from 'dayjs';

import * as actions from '@redux-news/news/newsActions';
import * as newsApiService from '@redux-news/news/newsApiService';

import { Card, CardBody, CardHeader, CardHeaderToolbar, ModalProgressBar } from '@metronic-partials/controls';
import { makeMaterialCategoryTree, makeProductCategoryTree } from '@metronic-helpers';

import {
  getNewsCategoriesTopicsIds,
  initialValuesForRelevantOrganization,
  useOrganizationsValues,
  NEWS,
} from '@common';
import { permissionsRoutePath } from '@common/Permissions/routesPaths';

import { NewsSelectForm } from './NewsSelectForm';
import { SelectedNews } from './SelectedNews';

export function NewsSelect() {
  const { id } = useParams();
  const history = useHistory();
  const dispatch = useDispatch();

  const [initNews, setInitNews] = useState(null);

  const [isSubmitting, setSubmitting] = useState(false);

  const [body, setBody] = useState('');

  const [newsDocs, setNewsDocs] = useState([]);
  const [newsDocTypes, setNewsDocTypes] = useState([]);

  const [regionList, setRegionList] = useState([]);
  const [categoryList, setCategoryList] = useState([]);
  const [productCategoriesTree, setProductCategoriesTree] = useState([]);
  const [materialCategoriesTree, setMaterialCategoriesTree] = useState([]);

  const [relevantOrganizationsValues, updateRelevantOrganizationsValues] = useOrganizationsValues(
    initialValuesForRelevantOrganization,
  );

  const { actionsLoading, newsForSelect, sourceList } = useSelector(state => ({
    actionsLoading: state.news.actionsLoading,
    newsForSelect: state.news.newsForSelect,
    sourceList: state.news.sourceList,
  }));

  const title = `Select news '${newsForSelect?.title || ''}'`;

  useEffect(() => {
    dispatch(actions.fetchSourceList());
    dispatch(actions.selectNews(id));
  }, [id, dispatch]);

  useEffect(() => {
    if (newsForSelect) {
      const productCategoriesIds = newsForSelect.product_categories.map(item => item.id);
      const materialCategoriesIds = newsForSelect.material_categories.map(item => item.id);
      const regulationsIds = newsForSelect.regulations.map(item => item.id);
      const regulatoryFrameworksIds = newsForSelect.regulatory_frameworks.map(item => item.id);

      setInitNews({
        ...newsForSelect,
        product_categories: productCategoriesIds,
        material_categories: materialCategoriesIds,
        regulations: regulationsIds,
        regulatory_frameworks: regulatoryFrameworksIds,
      });

      updateRelevantOrganizationsValues({
        product_categories: productCategoriesIds,
        material_categories: materialCategoriesIds,
        topics: getNewsCategoriesTopicsIds(newsForSelect.news_categories),
        regulations: regulationsIds,
        frameworks: regulatoryFrameworksIds,
      });
    }
  }, [newsForSelect, updateRelevantOrganizationsValues]);

  useEffect(() => {
    if (newsForSelect && !isSubmitting) {
      setBody(newsForSelect.body);

      newsApiService
        .getNewsBodyDocs(newsForSelect.id)
        .then(response => setNewsDocs(response.data))
        .catch(error => console.error(error));

      newsApiService.getRegionList().then(response => setRegionList(response.data.results));

      newsApiService.getCategoryList().then(response => setCategoryList(response.data.results));

      newsApiService
        .getDocumentTypeList()
        .then(response => setNewsDocTypes(response.data.results))
        .catch(error => console.error(error));

      newsApiService
        .getIndustries()
        .then(response => {
          const industries = response.data.results;

          const productCategoryTree = makeProductCategoryTree(industries);
          setProductCategoriesTree(productCategoryTree);

          const materialCategoryTree = makeMaterialCategoryTree(industries);
          setMaterialCategoriesTree(materialCategoryTree);
        })
        .catch(error => console.error(error));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [newsForSelect, id, isSubmitting]);

  const backToNewsList = () => history.push(`${permissionsRoutePath[NEWS]}/news`);

  const saveNews = (values, field) => {
    if (field && id) {
      if (field === 'body') {
        const { doc, data } = values;

        const newBody = body.replace(doc.link, data);

        dispatch(actions.selectNewsPatch(id, { body: newBody })).then(() => {
          setBody(newBody);
          setNewsDocs(prevState => prevState.filter(({ link }) => link !== doc.link));
        });
      } else if (field === 'finish news selection' || field === 'discharge') {
        setSubmitting(true);

        const dataToUpdate = values
          ? {
              title: values.title,
              pub_date: dayjs(values.pub_date)
                .format('YYYY-MM-DD')
                .concat('T00:00:00'),
              regulations: values.regulations,
              regulatory_frameworks: values.regulatory_frameworks,
              regions: values.regions ? values.regions.map(region => region.id) : [],
              news_categories: values.news_categories
                ? values.news_categories.map(news_category => news_category.id)
                : [],
              source: values.source.id,
              active: values.active,
              status: 's',
              product_categories: values.productChecked,
              material_categories: values.materialChecked,
            }
          : {
              status: 'd',
            };

        dispatch(actions.selectNewsPatch(id, dataToUpdate))
          .then(() => backToNewsList())
          .catch(error => {
            setSubmitting(false);
            console.error(error);
          });
      }
    }
  };

  return (
    <>
      <Card>
        {actionsLoading && <ModalProgressBar />}
        <CardHeader title={title} />

        <CardBody>
          <SelectedNews body={body} substances={initNews?.substances || []} />
        </CardBody>
      </Card>

      <Card>
        {actionsLoading && <ModalProgressBar />}
        <CardHeader title={title}>
          <CardHeaderToolbar>
            <button type="button" onClick={backToNewsList} className="btn btn-light">
              <i className="fa fa-arrow-left" />
              Back
            </button>
          </CardHeaderToolbar>
        </CardHeader>
        <CardBody>
          {!!initNews?.id && (
            <NewsSelectForm
              news={initNews}
              sourceList={sourceList}
              saveNews={saveNews}
              newsDocs={newsDocs}
              newsDocTypes={newsDocTypes}
              productCategoriesTree={productCategoriesTree}
              materialCategoriesTree={materialCategoriesTree}
              categoryList={categoryList}
              regionList={regionList}
              isSubmitting={isSubmitting}
              relevantOrganizationsValues={relevantOrganizationsValues}
              updateRelevantOrganizationsValues={updateRelevantOrganizationsValues}
            />
          )}
        </CardBody>
      </Card>
    </>
  );
}
