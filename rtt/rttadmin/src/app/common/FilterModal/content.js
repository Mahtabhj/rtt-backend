export const title = {
  news: 'News',
  regulation: 'Regulations'
};

export const filterItems = {
  news: [
    {
      label: 'Regions',
      name: 'regions',
      options: 'regionList',
    },
    {
      label: 'News Category',
      name: 'news_categories',
      options: 'categoryList',
    },
    {
      label: 'Product Category',
      name: 'product_categories',
      options: 'newsProductCategoryList',
    },
  ],
  regulation: [
    {
      label: 'Regulatory Framework',
      name: 'regulatory_framework',
      options: 'regulatoryFrameworkList',
      multi: false,
    },
    {
      label: 'Regulation Type',
      name: 'type',
      options: 'regulationTypeList',
    },
    {
      label: 'Review Status',
      name: 'review_status',
      options: 'reviewStatusOptions',
      multi: false,
    },
  ],
  regulatoryFramework: [
    {
      label: 'Issuing Body',
      name: 'issuing_body',
      options: 'issuingBodyList',
      multi: false
    },
    {
      label: 'Status',
      name: 'status',
      options: 'statusList',
      multi: false
    },
    {
      label: 'Regions',
      name: 'regions',
      options: 'issuingBodyRegionList',
    },
    {
      label: 'Material Category',
      name: 'material_categories',
      options: 'materialCategoryList',
    },
    {
      label: 'Product Category',
      name: 'product_categories',
      options: 'productCategoryList',
    },
    {
      label: 'Review Status',
      name: 'review_status',
      options: 'reviewStatusOptions',
      multi: false
    },
  ]
}

export const reviewStatusOptions = [
  {
    name: 'Online',
    id: 'o',
  },
  {
    name: 'Draft',
    id: 'd',
  }
];
