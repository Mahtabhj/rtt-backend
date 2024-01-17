import dayjs from 'dayjs';

export const formatDateDDMMYYY = (date) => dayjs(date).format("DD/MM/YYYY");

const formatArrayOfNames = (arrayOfNames) => {
  const arrayOfNamesNames = arrayOfNames?.map(category => category?.name);

  return arrayOfNamesNames?.join(', ');
}

export const formatCategoriesNames = (categories) => formatArrayOfNames(categories);

export const formatRegionsNames = (regions) => formatArrayOfNames(regions);

export const formatRegulationsNames = (regulations) => formatArrayOfNames(regulations);

export const formatFrameworksNames = (frameworks) => formatArrayOfNames(frameworks);

export const formatProductCategoriesNames = (productCategories) => formatArrayOfNames(productCategories);

export const formatMaterialCategoriesNames = (materialCategories) => formatArrayOfNames(materialCategories);