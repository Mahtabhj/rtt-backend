import React, { useMemo } from 'react';
import PropTypes from 'prop-types';

import { SelectCategories } from './SelectCategories';

const propTypes = {
  productCategoriesTree: PropTypes.arrayOf(PropTypes.object).isRequired,
  productChecked: PropTypes.arrayOf(PropTypes.number).isRequired,
  setProductChecked: PropTypes.func.isRequired,
  materialCategoriesTree: PropTypes.arrayOf(PropTypes.object).isRequired,
  materialChecked: PropTypes.arrayOf(PropTypes.number).isRequired,
  setMaterialChecked: PropTypes.func.isRequired,
  disabledCheckbox: PropTypes.bool,
  isForcedUpdate: PropTypes.bool
}

const defaultProps = {
  disabledCheckbox: false,
  isForcedUpdate: false,
}

export const SelectTreeView = ({
  productCategoriesTree,
  productChecked,
  setProductChecked,
  materialCategoriesTree,
  materialChecked,
  setMaterialChecked,
  disabledCheckbox,
  isForcedUpdate
}) => {
  const productExpandMap = useMemo(() => {
    if (productCategoriesTree.length) {
      const productExpandMap = {};

      productCategoriesTree.forEach(productCategory =>
        productCategory.children.forEach(productFirstNest => {
            if (productFirstNest.value) {
              productExpandMap[productFirstNest.value] = [productCategory.value];
            }

            productFirstNest.children && productFirstNest.children.forEach(productSecondNest => {
              if (productSecondNest.value) {
                productExpandMap[productSecondNest.value] = [productFirstNest.value, productCategory.value];
              }

              productSecondNest.children && productSecondNest.children.forEach(productThirdNest => {
                if (productThirdNest.value) {
                  productExpandMap[productThirdNest.value] =
                    [productSecondNest.value, productFirstNest.value, productCategory.value];
                }
              })
            })
          }
        )
      );

      return productExpandMap;
    }
  }, [productCategoriesTree]);

  const materialExpandMap = useMemo(() => {
    if (materialCategoriesTree.length) {
      const materialExpandMap = {};

      materialCategoriesTree.forEach(materialCategory =>
        materialCategory.children.forEach(materialChild => {
            if (materialChild.value) {
              materialExpandMap[materialChild.value] = [materialCategory.value]
            }
          }
        )
      );

      return materialExpandMap;
    }
  }, [materialCategoriesTree]);

  return !!(productExpandMap && materialExpandMap) && (
    <div className="form-group row mb-0 pt-10">
      <SelectCategories
        title='Select Product Categories'
        categoriesTree={productCategoriesTree}
        checked={productChecked}
        setChecked={setProductChecked}
        expandMap={productExpandMap}
        isForcedUpdate={isForcedUpdate}
        disabled={disabledCheckbox}
      />
      <SelectCategories
        title='Select Material Categories'
        categoriesTree={materialCategoriesTree}
        checked={materialChecked}
        setChecked={setMaterialChecked}
        expandMap={materialExpandMap}
        isForcedUpdate={isForcedUpdate}
        disabled={disabledCheckbox}
      />
    </div>
  );
}

SelectTreeView.propTypes = propTypes;
SelectTreeView.defaultProps = defaultProps;
