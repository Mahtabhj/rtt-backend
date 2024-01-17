import React, { useCallback, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import RichTextEditor from 'react-rte';
import { Modal } from 'react-bootstrap';

import * as actions from '@redux-regulation/regulatory-framework/regulatoryFrameworkActions';
import { getIndustries } from '@redux-news/news/newsApiService';

import { ModalProgressBar } from '@metronic-partials/controls';
import { makeMaterialCategoryTree, makeProductCategoryTree } from '@metronic-helpers';
import { SelectTreeView } from '@common';

import { RegulationForm } from './RegulationForm';

const initRegulationConst = {
  name: '',
  description: RichTextEditor.createEmptyValue(),
  review_status: 'd',
  type: '',
  language: '',
  status: '',
};

export const RegulationAddModalButton = ({ regulatoryFrameworkId }) => {
  const dispatch = useDispatch();

  const [isModalShown, setModalShown] = useState(false);

  const [initRegulation, setInitRegulation] = useState(initRegulationConst);

  const [productCategoriesTree, setProductCategoriesTree] = useState([]);
  const [materialCategoriesTree, setMaterialCategoriesTree] = useState([]);

  const [productChecked, setProductChecked] = useState([]);
  const [materialChecked, setMaterialChecked] = useState([]);

  const {
    parentRegulatoryFramework,
    actionsLoading,
    regulationTypeList,
    languageList,
    statusList,
    success,
  } = useSelector(state => ({
    parentRegulatoryFramework: state.regulatoryFramework.regulatoryFrameworkForEdit,
    actionsLoading: state.regulatoryFramework.actionsLoading,
    regulationTypeList: state.regulatoryFramework.regulationTypeList,
    languageList: state.regulatoryFramework.languageList,
    statusList: state.regulatoryFramework.statusList,
    success: state.regulatoryFramework.success,
  }));

  useEffect(() => {
    if (regulationTypeList && languageList && statusList) {
      const newInitRegulation = {
        ...initRegulationConst,
        type: regulationTypeList[0]?.id || null,
        language: languageList[0]?.id || null,
        status: statusList[0]?.id || null,
      };

      setInitRegulation(newInitRegulation);
    }
  }, [regulationTypeList, languageList, statusList]);

  useEffect(() => {
    let isSubscribed = true;

    getIndustries()
      .then(response => {
        const industries = response.data.results;

        const productCategoryTree = makeProductCategoryTree(industries);
        if (isSubscribed) setProductCategoriesTree(productCategoryTree);

        const materialCategoryTree = makeMaterialCategoryTree(industries);
        if (isSubscribed) setMaterialCategoriesTree(materialCategoryTree);
      })
      .catch(error => {
        console.error(error);
      });

    return () => {
      isSubscribed = false;
    };
  }, [dispatch]);

  useEffect(() => {
    const { product_categories, material_categories } = parentRegulatoryFramework;

    setProductChecked(product_categories.map(({ id }) => id));
    setMaterialChecked(material_categories.map(({ id }) => id));
  }, [parentRegulatoryFramework, isModalShown]);

  useEffect(() => {
    if (success) setModalShown(false);
  }, [success, setModalShown]);

  const handleOnOpen = () => setModalShown(true);

  const handleOnHide = useCallback(() => setModalShown(false), []);

  const saveRegulatoryFrameworkRelatedRegulation = useCallback(
    values => {
      const isDescriptionEmpty = values.description.toString('markdown').trim() === '\u200b';

      const submitValues = {
        ...values,
        product_categories: productChecked,
        material_categories: materialChecked,
        description: isDescriptionEmpty ? '' : values.description.toString('html'),
      };

      dispatch(
        actions.createRegulatoryFrameworkRelatedRegulation({
          ...submitValues,
          regulatory_framework: regulatoryFrameworkId,
        }),
      ).then(() => setModalShown(false));
    },
    [dispatch, regulatoryFrameworkId, productChecked, materialChecked],
  );

  return (
    <>
      <button type="button" className="btn btn-primary" onClick={handleOnOpen}>
        New Regulation
      </button>

      <Modal size="lg" show={isModalShown} onHide={handleOnHide} aria-labelledby="example-modal-sizes-title-lg">
        {actionsLoading && <ModalProgressBar variant="query" />}

        <Modal.Header closeButton>
          <Modal.Title id="example-modal-sizes-title-lg">Add Regulatory Framework Regulation</Modal.Title>
        </Modal.Header>

        <RegulationForm
          regulation={initRegulation}
          onSave={saveRegulatoryFrameworkRelatedRegulation}
          onCancel={handleOnHide}
          actionsLoading={actionsLoading}
        >
          <SelectTreeView
            productCategoriesTree={productCategoriesTree}
            productChecked={productChecked}
            setProductChecked={setProductChecked}
            materialCategoriesTree={materialCategoriesTree}
            materialChecked={materialChecked}
            setMaterialChecked={setMaterialChecked}
          />
        </RegulationForm>
      </Modal>
    </>
  );
};
