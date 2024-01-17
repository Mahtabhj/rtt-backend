/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid,jsx-a11y/role-supports-aria-props */
import React, { useEffect, useState, useRef, useMemo, useCallback } from 'react';
import { useHistory, useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import RichTextEditor from 'react-rte';

import * as actions from '@redux-regulation/regulation/regulationActions';
import { getIndustries } from '@redux-news/news/newsApiService';

import { Card, CardBody, CardHeader, CardHeaderToolbar, ModalProgressBar } from '@metronic-partials/controls';
import { makeMaterialCategoryTree, makeProductCategoryTree } from '@metronic-helpers';
import {
  getSuperuserKeyFromJwt,
  initialValuesForRelevantOrganization,
  toastInfoProlonged,
  useOrganizationsValues,
  useRegulationTaggedCategories,
  RelatedSubstances,
  SelectTreeView,
  TabMenu,
  VisibleToOrganization,
  DOCUMENT,
  REGULATION,
  TAB_DOCUMENTS,
  TAB_IMPACT_ASSESSMENT,
  TAB_MILESTONES,
  TAB_RELATED_SUBSTANCES,
  TAB_USEFUL_LINKS,
} from '@common';
import { AuthorizeDocument } from '@common/Permissions/AuthorizeWrappers';

import RegulationEditForm from './RegulationEditForm';
import { UrlTable } from '../related-url-table/UrlTable';
import { DocumentsTable } from '../related-documents-table/DocumentsTable';
import { ImpactAssessmentTable } from '../impact-assessment/ImpactAssessmentTable';
import { MilestoneTable } from '../milestone-table/MilestoneTable';

const relevantOrganizationsValuesInitialState = {
  product_categories: initialValuesForRelevantOrganization.product_categories,
  material_categories: initialValuesForRelevantOrganization.material_categories,
  topics: initialValuesForRelevantOrganization.topics,
};

const constInitRegulation = {
  id: undefined,
  name: '',
  type: '',
  status: '',
  review_status: 'o',
  description: RichTextEditor.createEmptyValue(),
  regulatory_framework: '',
  documents: [],
  language: '',
  urls: [],
  topics: [],
};

export function RegulationEdit() {
  const btnRef = useRef();
  const { id } = useParams();
  const history = useHistory();
  const dispatch = useDispatch();

  const [tab, setTab] = useState(TAB_USEFUL_LINKS);

  const [initRegulation, setInitRegulation] = useState(constInitRegulation);

  const [productCategoriesTree, setProductCategoriesTree] = useState([]);
  const [materialCategoriesTree, setMaterialCategoriesTree] = useState([]);

  const [isTreeViewForcedUpdate, setTreeViewForcedUpdate] = useState(false);

  const [relevantOrganizationsValues, updateRelevantOrganizationsValues] = useOrganizationsValues(
    relevantOrganizationsValuesInitialState,
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

  const getRegulationTaggedCategoriesCallback = useCallback(
    ({ taggedName, product_categories, material_categories }) => {
      const newProductCount = product_categories.filter(checkedId => !allProductChecked.includes(checkedId)).length;
      const newMaterialCount = material_categories.filter(checkedId => !allMaterialChecked.includes(checkedId)).length;
      const total = newMaterialCount + newProductCount;

      const getToastMessage = () => {
        const importedCategoriesClarification = `${newProductCount ? `${newProductCount} product` : ''}${
          newProductCount && newMaterialCount ? ', ' : ''
        }${newMaterialCount ? `${newMaterialCount} material` : ''}`;

        return `${total} ${total ? `(${importedCategoriesClarification}) ` : ''}${
          total > 1 || !total ? 'categories' : 'category'
        } have been imported from "${taggedName}" regulatory framework`;
      };

      if (total) toastInfoProlonged(getToastMessage());

      updateRegulationTaggedCategoriesCallback({ product_categories, material_categories });
    },
    [allProductChecked, allMaterialChecked, updateRegulationTaggedCategoriesCallback],
  );

  const {
    actionsLoading,
    regulationForEdit,
    documentList,
    urlList,
    statusList,
    languageList,
    regulatoryFrameworkList,
    regulationTypeList,
    topicList,
    isSuperuser,
    isDocumentAccessAllowed,
  } = useSelector(state => ({
    actionsLoading: state.regulation.actionsLoading,
    regulationForEdit: state.regulation.regulationForEdit,
    documentList: state.regulation.documentList,
    urlList: state.regulation.urlList,
    statusList: state.regulation.statusList,
    languageList: state.regulation.languageList,
    regulatoryFrameworkList: state.regulation.regulatoryFrameworkList,
    regulationTypeList: state.regulation.regulationTypeList,
    topicList: state.regulation.topicList,
    isSuperuser: getSuperuserKeyFromJwt(state.auth.authToken),
    isDocumentAccessAllowed: state.auth.permissions.includes(DOCUMENT),
  }));

  const substancesQueryParams = useMemo(() => ({ regulation_id: id }), [id]);

  useEffect(() => {
    // get dropdown options
    dispatch(actions.fetchRegulationTypeList());
    dispatch(actions.fetchRegulatoryFrameworkList());
    dispatch(actions.fetchStatusList());
    dispatch(actions.fetchLanguageList());
    dispatch(actions.fetchDocumentsList());
    dispatch(actions.fetchURLsList());
    dispatch(actions.fetchTopicList());
  }, [dispatch]);

  useEffect(() => {
    getIndustries()
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
    if (id) {
      dispatch(actions.fetchRegulation(id));
      dispatch(actions.fetchRegulationImpactAssessment(id));
      dispatch(actions.fetchRegulationImpactAssessmentAnswers(id));
    } else {
      dispatch(actions.dropRegulationForEdit());
    }
  }, [id, dispatch]);

  useEffect(() => {
    if (id && regulationForEdit) {
      const {
        description,
        product_categories: productCategories,
        material_categories: materialCategories,
        topics,
      } = regulationForEdit;

      const newRegulationForEdit = {
        ...regulationForEdit,
        description: RichTextEditor.createValueFromString(description, 'html'),
      };

      const productCategoryIds = productCategories.map(item => item.id);
      const materialCategoryIds = materialCategories.map(item => item.id);
      const topicIds = topics.map(item => item.id);

      new Promise(resolve => {
        setTreeViewForcedUpdate(true);
        setProductChecked(productCategoryIds);
        setMaterialChecked(materialCategoryIds);

        resolve();
      }).then(() => setTreeViewForcedUpdate(false));

      updateRelevantOrganizationsValues({
        product_categories: productCategoryIds,
        material_categories: materialCategoryIds,
        topics: topicIds,
      });

      setInitRegulation(newRegulationForEdit);
    } else {
      setInitRegulation(constInitRegulation);
    }
  }, [id, regulationForEdit, setProductChecked, setMaterialChecked, updateRelevantOrganizationsValues]);

  const isDropdownOptionsLoaded = !!(
    documentList &&
    urlList &&
    statusList &&
    regulatoryFrameworkList &&
    languageList &&
    regulationTypeList &&
    topicList
  );

  const saveRegulationClick = () => btnRef?.current?.click();

  const backToRegulationList = () => history.push(`/backend/regulation-info/regulation`);

  const saveRegulation = values => {
    const isDescriptionEmpty = values.description.toString('markdown').trim() === '\u200b';

    const submitValue = {
      ...values,
      documents: values.documents ? values.documents.map(doc => doc.id) : [],
      product_categories: allProductChecked,
      material_categories: allMaterialChecked,
      urls: values.urls ? values.urls.map(url => url.id) : [],
      review_status: values.review_status,
      language: values.language.id,
      type: values.type.id,
      status: values.status.id,
      regulatory_framework: values.regulatory_framework.id,
      topics: values.topics ? values.topics.map(topic => topic.id) : [],
      description: isDescriptionEmpty ? '' : values.description.toString('html'),
    };

    delete submitValue.substances;

    dispatch((id ? actions.updateRegulation : actions.createRegulation)(submitValue)).then(() =>
      backToRegulationList(),
    );
  };

  return (
    <>
      {isDropdownOptionsLoaded && !actionsLoading ? (
        <Card>
          <CardHeader title={initRegulation.id ? `Edit Regulation: ${initRegulation.name}` : 'Create Regulation'}>
            <CardHeaderToolbar>
              <button type="button" onClick={backToRegulationList} className="btn btn-light">
                <i className="fa fa-arrow-left" />
                Back
              </button>
              <button type="submit" className="btn btn-primary ml-2" onClick={saveRegulationClick}>
                Save
              </button>
            </CardHeaderToolbar>
          </CardHeader>
          <CardBody>
            <div className="mt-5">
              <RegulationEditForm
                regulation={initRegulation}
                updateRelevantOrganizationsValues={updateRelevantOrganizationsValues}
                btnRef={btnRef}
                saveRegulation={saveRegulation}
                statusList={statusList || []}
                regulatoryFrameworkList={regulatoryFrameworkList || []}
                languageList={languageList || []}
                regulationTypeList={regulationTypeList || []}
                topicList={topicList || []}
                getRegulationTaggedCategoriesCallback={getRegulationTaggedCategoriesCallback}
              />
            </div>

            <SelectTreeView
              productCategoriesTree={productCategoriesTree}
              productChecked={allProductChecked}
              setProductChecked={handleProductsChecked}
              materialCategoriesTree={materialCategoriesTree}
              materialChecked={allMaterialChecked}
              setMaterialChecked={handleMaterialsChecked}
              isForcedUpdate={isTreeViewForcedUpdate}
            />

            <VisibleToOrganization type={REGULATION} valuesForRelevantOrganizations={relevantOrganizationsValues} />
          </CardBody>
        </Card>
      ) : (
        <ModalProgressBar />
      )}

      {!!id && !!regulationForEdit && (
        <Card>
          <CardBody>
            <TabMenu
              options={
                isSuperuser || isDocumentAccessAllowed
                  ? [TAB_USEFUL_LINKS, TAB_DOCUMENTS, TAB_MILESTONES, TAB_IMPACT_ASSESSMENT, TAB_RELATED_SUBSTANCES]
                  : [TAB_USEFUL_LINKS, TAB_MILESTONES, TAB_IMPACT_ASSESSMENT, TAB_RELATED_SUBSTANCES]
              }
              selected={tab}
              onSelect={setTab}
            />

            <div className="mt-5">
              {tab === TAB_USEFUL_LINKS && <UrlTable regulationId={id} />}

              <AuthorizeDocument>{tab === TAB_DOCUMENTS && <DocumentsTable regulationId={id} />}</AuthorizeDocument>

              {tab === TAB_MILESTONES && <MilestoneTable regulationId={id} />}
              {tab === TAB_IMPACT_ASSESSMENT && <ImpactAssessmentTable regulationId={id} />}
              {tab === TAB_RELATED_SUBSTANCES && <RelatedSubstances queryParams={substancesQueryParams} isCard />}
            </div>
          </CardBody>
        </Card>
      )}
    </>
  );
}
