import React, { useEffect, useMemo, useState, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import RichTextEditor from "react-rte";

import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import * as issuing_actions from "@redux-regulation/issuingbody/issuingbodyActions";
import { getIndustries } from "@redux-news/news/newsApiService";

import { Card, CardBody, CardHeader, CardHeaderToolbar, ModalProgressBar } from "@metronic-partials/controls";
import { makeMaterialCategoryTree, makeProductCategoryTree } from "@metronic-helpers";
import {
  getSuperuserKeyFromJwt,
  initialValuesForRelevantOrganization,
  RelatedSubstances,
  SelectTreeView,
  TabMenu,
  VisibleToOrganization,
  DOCUMENT,
  REGULATION,
  REGULATORY_FRAMEWORK,
  TAB_DOCUMENTS,
  TAB_IMPACT_ASSESSMENT,
  TAB_MILESTONES,
  TAB_RELATED_REGULATIONS,
  TAB_RELATED_SUBSTANCES,
  TAB_USEFUL_LINKS,
} from "@common";
import { AuthorizeDocument, AuthorizeRegulation } from "@common/Permissions/AuthorizeWrappers";

import RegulatoryFrameworkEditForm from "./RegulatoryFrameworkEditForm";
import { RegulationTable } from "../related-regulation-table/RegulationTable";
import { LinkTable } from "../useful-link-table/LinkTable";
import { MilestoneTable } from "../milestone-table/MilestoneTable";
import { ImpactAssessmentTable } from "../impact-assessment/ImpactAssessmentTable";
import { DocumentsTable } from "../related-documents-table/DocumentsTable";
import { useOrganizationsValues } from "../../../../../common";

const constInitFramework = {
  id: undefined,
  name: "",
  review_status: "d",
  status: "",
  language: "",
  description: RichTextEditor.createEmptyValue(),
  issuing_body: null,
  regions: [],
  documents: [],
  urls: [],
  topics: [],
};

const relevantOrganizationsValuesInitialState = {
  product_categories: initialValuesForRelevantOrganization.product_categories,
  material_categories: initialValuesForRelevantOrganization.material_categories,
  regulations: initialValuesForRelevantOrganization.regulations,
  topics: initialValuesForRelevantOrganization.topics,
};

export function RegulatoryFrameworkEdit({ match: { params: { id } } }) {
  const btnRef = useRef();
  const history = useHistory();
  const dispatch = useDispatch();

  const [tab, setTab] = useState(TAB_RELATED_REGULATIONS);

  const [initRegulatoryFramework, setInitRegulatoryFramework] = useState(constInitFramework);

  const [productCategoriesTree, setProductCategoriesTree] = useState([]);
  const [materialCategoriesTree, setMaterialCategoriesTree] = useState([]);

  const [productChecked, setProductChecked] = useState([]);
  const [materialChecked, setMaterialChecked] = useState([]);

  const [relevantOrganizationsValues, updateRelevantOrganizationsValues] = useOrganizationsValues(
    relevantOrganizationsValuesInitialState,
  );

  const {
    actionsLoading,
    regulatoryFrameworkForEdit,
    languageList,
    statusList,
    regionList,
    topicList,
    isSuperuser,
    isRegulationAccessAllowed,
    isDocumentAccessAllowed,
  } = useSelector(
    (state) => ({
      actionsLoading: state.regulatoryFramework.actionsLoading,
      regulatoryFrameworkForEdit: state.regulatoryFramework.regulatoryFrameworkForEdit,
      languageList: state.regulatoryFramework.languageList,
      statusList: state.regulatoryFramework.statusList,
      regionList: state.issuingbody.regionList,
      topicList: state.regulatoryFramework.topicList,
      isSuperuser: getSuperuserKeyFromJwt(state.auth.authToken),
      isRegulationAccessAllowed: state.auth.permissions.includes(REGULATION),
      isDocumentAccessAllowed: state.auth.permissions.includes(DOCUMENT),
    })
  );

  const tabMenuOptions = useMemo(() => {
    const options = [
      TAB_RELATED_REGULATIONS,
      TAB_USEFUL_LINKS,
      TAB_DOCUMENTS,
      TAB_MILESTONES,
      TAB_IMPACT_ASSESSMENT,
      TAB_RELATED_SUBSTANCES
    ];

    if (isSuperuser) {
      return options;
    } else {
      const deniedTabs = [];

      if (!isRegulationAccessAllowed) deniedTabs.push(TAB_RELATED_REGULATIONS);
      if (!isDocumentAccessAllowed) deniedTabs.push(TAB_DOCUMENTS);

      return options.filter(option => !deniedTabs.includes(option));
    }
  }, [isSuperuser, isRegulationAccessAllowed, isDocumentAccessAllowed]);

  const substancesQueryParams = useMemo(() => ({ regulatory_framework_id: id }), [id]);

  useEffect(() => {
    dispatch(actions.fetchRegulatoryFramework(id));
    dispatch(actions.fetchRegulatoryFrameworkImpactAssessment(id));
    dispatch(actions.fetchUserList());
    if (id) {
      dispatch(actions.fetchRelatedRegulationList(id));
      dispatch(actions.fetchRegulatoryFrameworkImpactAssessmentAnswers(id));
    }
  }, [id, dispatch]);

  useEffect(() => {
    dispatch(actions.fetchLanguageList());
    dispatch(actions.fetchStatusList());
    dispatch(actions.fetchRegulationTypeList());
    dispatch(actions.fetchLinkList());
    dispatch(actions.fetchDocumentsList());
    dispatch(actions.fetchTopicList());
    dispatch(issuing_actions.fetchRegionList());
  }, [dispatch]);

  useEffect(() => {
    getIndustries()
      .then((response) => {
        const industries = response.data.results;

        const productCategoryTree = makeProductCategoryTree(industries);
        setProductCategoriesTree(productCategoryTree);

        const materialCategoryTree = makeMaterialCategoryTree(industries);
        setMaterialCategoriesTree(materialCategoryTree);
      })
      .catch((error) => {
        console.error(error);
      })
  }, [dispatch]);

  useEffect(() => {
    if (id && regulatoryFrameworkForEdit) {
      const {
        issuing_body: issuingBody,
        description,
        product_categories: productCategories,
        material_categories: materialCategories,
        regulation_regulatory_framework: regulationRegulatoryFramework,
        topics,
      } = regulatoryFrameworkForEdit;

      const newRegulatoryFrameworkForEdit = {
        ...regulatoryFrameworkForEdit,
        issuing_body: issuingBody?.id || null,
        description: RichTextEditor.createValueFromString(description, "html"),
      };

      const productCategoryIds = productCategories.map(item => item.id);
      const materialCategoryIds = materialCategories.map(item => item.id);
      const regulationIds = regulationRegulatoryFramework.map(item => item.id);
      const topicIds = topics.map(item => item.id);

      setProductChecked(productCategoryIds);
      setMaterialChecked(materialCategoryIds);

      updateRelevantOrganizationsValues({
        product_categories: productCategoryIds,
        material_categories: materialCategoryIds,
        regulations: regulationIds,
        topics: topicIds,
      });

      setInitRegulatoryFramework(newRegulatoryFrameworkForEdit);
    } else {
      setInitRegulatoryFramework(constInitFramework);
    }
  }, [id, regulatoryFrameworkForEdit, setProductChecked, setMaterialChecked, updateRelevantOrganizationsValues]);

  const isDropdownOptionsLoaded = !!(statusList && languageList && topicList);

  const handleProductsChecked = productIds => {
    setProductChecked(productIds);

    updateRelevantOrganizationsValues({ product_categories: productIds });
  };

  const handleMaterialsChecked = materialIds => {
    setMaterialChecked(materialIds);

    updateRelevantOrganizationsValues({ material_categories: materialIds });
  };

  const saveRegulatoryFrameworkClick = () => btnRef?.current?.click();

  const backToRegulatoryFrameworkList = () => history.push(`/backend/regulation-info/regulatory-framework`);

  const toRegulatoryFrameworkEditPage = createdFrameworkId =>
    history.push(`/backend/regulation-info/regulatory-framework/${createdFrameworkId}/edit`);

  const saveRegulatoryFramework = values => {
    const isDescriptionEmpty = values.description.toString("markdown").trim() === '\u200b';

    const submitValue = {
      ...values,
      language: values.language.id,
      status: values.status.id,
      documents: values.documents ? values.documents.map((doc) => doc.id) : [],
      product_categories: productChecked.map((productCategoryId) => +productCategoryId),
      material_categories: materialChecked.map((materialCategoryId) => +materialCategoryId),
      urls: values.urls ? values.urls.map((url) => url.id) : [],
      regions: values.regions ? values.regions.map((region) => region.id) : [],
      topics: values.topics ? values.topics.map((topic) => topic.id) : [],
      description: isDescriptionEmpty ? '' : values.description.toString("html"),
    };

    delete submitValue.substances;

    if (!id) {
      dispatch(actions.createRegulatoryFramework(submitValue)).then(createdFrameworkId =>
        toRegulatoryFrameworkEditPage(createdFrameworkId)
      );
    } else {
      dispatch(actions.updateRegulatoryFramework(submitValue)).then(() =>
        backToRegulatoryFrameworkList()
      );
    }
  };

  return (
    <>
      {isDropdownOptionsLoaded && !actionsLoading ? (
        <Card>
          <CardHeader
            title={initRegulatoryFramework?.id ? `Edit Regulatory Framework: ${initRegulatoryFramework?.name}` : "Create Regulatory Framework"}
          >
            <CardHeaderToolbar>
              <button
                type="button"
                onClick={backToRegulatoryFrameworkList}
                className="btn btn-light"
              >
                <i className="fa fa-arrow-left"/>
                Back
              </button>
              <button
                type="submit"
                className="btn btn-primary ml-2"
                onClick={saveRegulatoryFrameworkClick}
              >
                Save
              </button>
            </CardHeaderToolbar>
          </CardHeader>
          <CardBody>
            <RegulatoryFrameworkEditForm
              regulatoryFramework={initRegulatoryFramework}
              updateRelevantOrganizationsValues={updateRelevantOrganizationsValues}
              btnRef={btnRef}
              saveRegulatoryFramework={saveRegulatoryFramework}
              languageList={languageList || []}
              statusList={statusList || []}
              regionList={regionList || []}
              topicList={topicList || []}
            />

            <SelectTreeView
              disabledCheckbox={false}
              productCategoriesTree={productCategoriesTree}
              productChecked={productChecked}
              setProductChecked={handleProductsChecked}
              materialCategoriesTree={materialCategoriesTree}
              materialChecked={materialChecked}
              setMaterialChecked={handleMaterialsChecked}
            />

            <VisibleToOrganization
              type={REGULATORY_FRAMEWORK}
              valuesForRelevantOrganizations={relevantOrganizationsValues}
            />
          </CardBody>
        </Card>
      ) : (
        <ModalProgressBar />
      )}

      {!!id && !!regulatoryFrameworkForEdit && (
        <Card>
          <CardBody>
            <TabMenu
              options={tabMenuOptions}
              selected={tab}
              onSelect={setTab}
            />

            <div className="mt-5">
              <AuthorizeRegulation>
                {tab === TAB_RELATED_REGULATIONS && (
                  <RegulationTable regulatoryFrameworkId={id} />
                )}
              </AuthorizeRegulation>
              {tab === TAB_USEFUL_LINKS && (
                <LinkTable regulatoryFrameworkId={id} />
              )}

              <AuthorizeDocument>
                {tab === TAB_DOCUMENTS && (
                  <DocumentsTable regulatoryFrameworkId={id} />
                )}
              </AuthorizeDocument>
              {tab === TAB_MILESTONES && (
                <MilestoneTable regulatoryFrameworkId={id} />
              )}
              {tab === TAB_IMPACT_ASSESSMENT && (
                <ImpactAssessmentTable regulatoryFrameworkId={id}
                />
              )}
              {tab === TAB_RELATED_SUBSTANCES && (
                <RelatedSubstances queryParams={substancesQueryParams} isCard />
              )}
            </div>
          </CardBody>
        </Card>
      )}
    </>
  );
}
