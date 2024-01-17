import { useCallback, useState } from 'react';
import { initialValuesForRelevantOrganization } from './constants';

const arraysAreEqual = (a, b) =>
  Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every((val, index) => val === b[index]);

// used with VisibleToOrganization
export const useOrganizationsValues = (initialState = initialValuesForRelevantOrganization) => {
  const [relevantOrganizationsValues, setRelevantOrganizationsValues] = useState(initialState);

  const updateRelevantOrganizationsValues = useCallback(
    values =>
      setRelevantOrganizationsValues(prevState => {
        const allowedValuesKeys = Object.keys(initialState);
        const valuesKeys = Object.keys(values);

        const isAllowedValues = valuesKeys.every(key => allowedValuesKeys.includes(key));
        const isValuesChanged = valuesKeys.some(key => !arraysAreEqual(values[key], prevState[key]));

        return isAllowedValues && isValuesChanged ? { ...prevState, ...values } : prevState;
      }),
    [initialState],
  );

  return [relevantOrganizationsValues, updateRelevantOrganizationsValues];
};

const SIZE_PER_PAGE_LIST = {
  100: [
    { text: '100', value: 100 },
    { text: '200', value: 200 },
    { text: '300', value: 300 },
  ],
};

export const usePaginationQuery = (totalSize, sizePerPage) => {
  const [paginationQuery, setPaginationQuery] = useState({
    page: 1,
    sizePerPage,
  });

  const customOptions = useCallback(
    (totalSizeValue, sizePerPageList) => ({
      totalSize: totalSizeValue,
      page: paginationQuery.page,
      sizePerPage: paginationQuery.sizePerPage,
      sizePerPageList: sizePerPageList[sizePerPage],
      hideSizePerPage: false,
    }),
    [sizePerPage, paginationQuery],
  );

  return [paginationQuery, setPaginationQuery, customOptions(totalSize, SIZE_PER_PAGE_LIST)];
};

const noop = () => {};

export const useFiltersQuery = (setPaginationQuery, dropSelectionCallback = noop) => {
  const [filtersQuery, setFiltersQuery] = useState(null);

  const onTableChange = useCallback(
    (type, { page, sizePerPage, filters }) => {
      if (type === 'pagination') {
        setPaginationQuery(prevState => ({ page: prevState.sizePerPage === sizePerPage ? page : 1, sizePerPage }));
      }
      if (type === 'filter') {
        const filterKeys = Object.keys(filters);
        const newFiltersEntries = filterKeys.map(key => [key, filters[key].filterVal]);
        const newFilters = Object.fromEntries(newFiltersEntries);

        setFiltersQuery(filterKeys.length ? newFilters : null);

        dropSelectionCallback();
      }
    },
    [setPaginationQuery, dropSelectionCallback],
  );

  return [filtersQuery, setFiltersQuery, onTableChange];
};

const getHandleChecked = (
  allChecked,
  setChecked,
  setRegulationTaggedChecked,
  updateRelevantOrganizationsValues,
  relevantOrganizationsValuesCategoriesName,
) => ids => {
  const removeId = allChecked.find(checkedId => !ids.includes(checkedId));
  const getAddId = () => ids.find(checkedId => !allChecked.includes(checkedId));
  const removeChecked = checkedState => checkedState.filter(checkedId => checkedId !== removeId);

  setRegulationTaggedChecked(regulationTaggedCheckedPrevState => {
    const isRegulationTaggedRemove = regulationTaggedCheckedPrevState.includes(removeId);

    // update categories checked by user
    setChecked(checkedPrevState => {
      const getUpdatedChecked = () => (isRegulationTaggedRemove ? checkedPrevState : [...checkedPrevState, getAddId()]);

      const newChecked = checkedPrevState.includes(removeId) ? removeChecked(checkedPrevState) : getUpdatedChecked();

      // relevantOrganizationsValuesCategoriesName: product_categories / material_categories
      updateRelevantOrganizationsValues({ [relevantOrganizationsValuesCategoriesName]: newChecked });

      return newChecked;
    });

    // update regulation tagged categories
    return isRegulationTaggedRemove
      ? removeChecked(regulationTaggedCheckedPrevState)
      : regulationTaggedCheckedPrevState;
  });
};

export const useRegulationTaggedCategories = (setTreeViewForcedUpdate, updateRelevantOrganizationsValues) => {
  const [productChecked, setProductChecked] = useState([]);
  const [materialChecked, setMaterialChecked] = useState([]);

  const [regulationTaggedProductChecked, setRegulationTaggedProductChecked] = useState([]);
  const [regulationTaggedMaterialChecked, setRegulationTaggedMaterialChecked] = useState([]);

  const updateRegulationTaggedCategoriesCallback = useCallback(
    ({ product_categories, material_categories }) =>
      new Promise(resolve => {
        setTreeViewForcedUpdate(true);
        setRegulationTaggedProductChecked(product_categories);
        setRegulationTaggedMaterialChecked(material_categories);

        resolve();
      }).then(() => setTreeViewForcedUpdate(false)),
    [setTreeViewForcedUpdate],
  );

  const allProductChecked = useCallback(() => [...new Set([...productChecked, ...regulationTaggedProductChecked])], [
    productChecked,
    regulationTaggedProductChecked,
  ])();

  const allMaterialChecked = useCallback(() => [...new Set([...materialChecked, ...regulationTaggedMaterialChecked])], [
    materialChecked,
    regulationTaggedMaterialChecked,
  ])();

  const handleProductsChecked = getHandleChecked(
    allProductChecked,
    setProductChecked,
    setRegulationTaggedProductChecked,
    updateRelevantOrganizationsValues,
    'product_categories',
  );

  const handleMaterialsChecked = getHandleChecked(
    allMaterialChecked,
    setMaterialChecked,
    setRegulationTaggedMaterialChecked,
    updateRelevantOrganizationsValues,
    'material_categories',
  );

  return {
    allProductChecked,
    setProductChecked,
    allMaterialChecked,
    setMaterialChecked,
    handleProductsChecked,
    handleMaterialsChecked,
    updateRegulationTaggedCategoriesCallback,
  };
};
