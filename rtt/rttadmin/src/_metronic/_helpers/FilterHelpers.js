export const prepareFilterQueryParams = (filterOptions) => {
  const filterKeys = Object.keys(filterOptions);

  const makeArrayIds = (value) => Array.isArray(value) ? value.map(item => item.id) : [value.id];

  const optionsEntries = filterKeys.map(filterKey => {
    const currentValue = filterOptions[filterKey];
    const valueIds = currentValue ? makeArrayIds(currentValue) : [];
    const filterValue = valueIds.length ? valueIds.join(',') : null;

    return [filterKey, filterValue]
  })

  return Object.fromEntries(optionsEntries);
};

export const isCurrentQueryParamsNotContainFilterQueryParams = (currentQueryParams, filterQueryParams) => {
  const filterParamsKeys = Object.keys(filterQueryParams);

  return filterParamsKeys.some(key => {
    if ((typeof currentQueryParams[key] === "undefined") && (filterQueryParams[key] === null)) {
      return false;
    } else {
      return currentQueryParams[key] !== filterQueryParams[key]
    }
  });
};

