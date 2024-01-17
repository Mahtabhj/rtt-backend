import { useCallback, useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import PropTypes from 'prop-types';

import { getRegulationTaggedCategories, showLastSelected } from '@redux/app/appActions';

const propTypes = {
  regulations: PropTypes.arrayOf(PropTypes.number).isRequired,
  frameworks: PropTypes.arrayOf(PropTypes.number).isRequired,
  materialCategories: PropTypes.arrayOf(PropTypes.number).isRequired,
  productCategories: PropTypes.arrayOf(PropTypes.number).isRequired,
  updateCategoriesCallback: PropTypes.func.isRequired,
};

export const RegulationTaggedCategories = ({
  regulations,
  frameworks,
  materialCategories,
  productCategories,
  updateCategoriesCallback,
}) => {
  const dispatch = useDispatch();

  const [, setSelected] = useState(null);

  const showImportedToast = useCallback(
    ({ selectedId, newMaterialCount, newProductCount, getFromTitle }) => {
      const total = newMaterialCount + newProductCount;

      const getToastMessage = title => {
        const importedCategoriesClarification = `${newProductCount ? `${newProductCount} product` : ''}${
          newProductCount && newMaterialCount ? ', ' : ''
        }${newMaterialCount ? `${newMaterialCount} material` : ''}`;

        return `${total} ${total ? `(${importedCategoriesClarification}) ` : ''}${
          total > 1 || !total ? 'categories' : 'category'
        } have been imported ${getFromTitle(title)}`;
      };

      if (total) {
        dispatch(showLastSelected({ selectedId, getToastMessage }));
      }
    },
    [dispatch],
  );

  useEffect(() => {
    // save preselected categories to state holding initial regulations and frameworks except unselected by user (updated after processing)
    // selected regulations & frameworks (updated after processing)
    // selected material & product categories
    setSelected(prevState => ({
      preselected_regulations: prevState ? prevState.preselected_regulations : regulations,
      preselected_frameworks: prevState ? prevState.preselected_frameworks : frameworks,
      regulations: prevState?.regulations,
      frameworks: prevState?.frameworks,
      material_categories: materialCategories,
      product_categories: productCategories,
    }));
  }, [regulations, frameworks, materialCategories, productCategories]);

  useEffect(() => {
    let isSubscribed = true;

    // processing
    setSelected(
      ({
        preselected_regulations: preselectedRegulations,
        preselected_frameworks: preselectedFrameworks,
        regulations: prevSelectedRegulations,
        frameworks: prevSelectedFrameworks,
        material_categories: selectedMaterialCategories,
        product_categories: selectedProductCategories,
      }) => {
        const filteredPreselectedRegulations = preselectedRegulations.filter(id => regulations.includes(id));
        const filteredPreselectedFrameworks = preselectedFrameworks.filter(id => frameworks.includes(id));

        const userSelectedRegulations = regulations.filter(id => !filteredPreselectedRegulations.includes(id));
        const userSelectedFrameworks = frameworks.filter(id => !filteredPreselectedFrameworks.includes(id));

        if (userSelectedRegulations.length || userSelectedFrameworks.length) {
          // do nothing if preselected removed
          if (
            preselectedRegulations.length === filteredPreselectedRegulations.length &&
            preselectedFrameworks.length === filteredPreselectedFrameworks.length
          ) {
            dispatch(
              getRegulationTaggedCategories({
                regulations: userSelectedRegulations,
                frameworks: userSelectedFrameworks,
              }),
            ).then(({ payload }) => {
              const { material_categories, product_categories } = payload;

              if (isSubscribed) {
                const newRegulationSelected = userSelectedRegulations.find(id => !prevSelectedRegulations.includes(id));
                const newFrameworkSelected = userSelectedFrameworks.find(id => !prevSelectedFrameworks.includes(id));

                const newMaterialCount = material_categories.filter(id => !selectedMaterialCategories.includes(id))
                  .length;
                const newProductCount = product_categories.filter(id => !selectedProductCategories.includes(id)).length;

                if (newRegulationSelected) {
                  const getFromTitle = title => `from "${title}" regulation`;

                  showImportedToast({
                    selectedId: newRegulationSelected,
                    newMaterialCount,
                    newProductCount,
                    getFromTitle,
                  });
                }

                if (newFrameworkSelected) {
                  const getFromTitle = title => `from "${title}" regulatory framework`;

                  showImportedToast({
                    selectedId: newFrameworkSelected,
                    newMaterialCount,
                    newProductCount,
                    getFromTitle,
                  });
                }

                updateCategoriesCallback({
                  product_categories,
                  material_categories,
                });
              }
            });
          }
        } else {
          updateCategoriesCallback({
            product_categories: [],
            material_categories: [],
          });
        }

        return {
          preselected_regulations: filteredPreselectedRegulations,
          preselected_frameworks: filteredPreselectedFrameworks,
          regulations,
          frameworks,
          material_categories: selectedMaterialCategories,
          product_categories: selectedProductCategories,
        };
      },
    );

    return () => {
      isSubscribed = false;
    };
  }, [dispatch, regulations, frameworks, updateCategoriesCallback, showImportedToast]);

  return null;
};

RegulationTaggedCategories.propTypes = propTypes;
