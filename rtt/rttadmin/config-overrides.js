const { alias } = require("react-app-rewire-alias");

module.exports = function override(config) {
  alias({
    "@common": "src/app/common",
    "@components": "src/app/modules",
    "@metronic": "src/_metronic",
    "@metronic-assets": "src/_metronic/_assets",
    "@metronic-helpers": "src/_metronic/_helpers",
    "@metronic-partials": "src/_metronic/_partials",
    "@redux": "src/redux",
    "@redux-auth": "src/app/modules/Auth/_redux",
    "@redux-document": "src/app/modules/DocumentInfo/_redux",
    "@redux-news": "src/app/modules/NewsInfo/_redux",
    "@redux-organization": "src/app/modules/OrganizationInfo/_redux",
    "@redux-product": "src/app/modules/ProductInfo/_redux",
    "@redux-regulation": "src/app/modules/RegulationInfo/_redux",
  })(config);

  return config;
};
