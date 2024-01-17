const DIRECTORY_ID_FACTOR = 1000;

export const makeProductCategoryTree = (industries) => industries.map(
  (industry) => {
    let validParents = industry.product_categories.filter(
      (category) => category.parent === null
    );

    const parents = validParents.map((parent) => {
      parent.children = [];

      industry.product_categories.forEach((category) => {
        if (category.parent === parent.id) {
          parent.children.push({
            ...category,
            value: category.id,
            label: category.name,
          })
        }
      });

      industry.product_categories.forEach((category) => {
        const child = parent.children.find(child => child.id === category.parent)

        if (child) {
          if (!child?.children) {
            child.children = [];
          }

          child.children.push({
            ...category,
            label: category.name,
            value: category.id,
          })
        }
      });

      return {
        ...parent,
        value: parent.id,
        label: parent.name,
        children: parent.children.length ? parent.children : null,
      }
    })

    return {
      value: industry.id * 6 * DIRECTORY_ID_FACTOR,
      label: industry.name,
      showCheckbox: false,
      children: parents,
    };
  }
  )
;

export const makeMaterialCategoryTree = (industries) => industries.map(
  (industry) => {
    const materialCategories = industry.material_categories.map(
      (materialCategory) => ({
        value: materialCategory.id,
        label: materialCategory.name,
      })
    );

    return {
      value: industry.id * 15 * DIRECTORY_ID_FACTOR,
      label: industry.name,
      showCheckbox: false,
      children: materialCategories,
    };
  }
);

