![](https://rtt-test.chemycal.com/static/logos/brand-logo.svg)

[//]: # (Product Comply React Admin Panel)
## React Admin Panel

- [app.productcomply.com/backend](https://app.productcomply.com/backend) production server
- [rtt-test.chemycal.com/backend](https://rtt-test.chemycal.com/backend) test server

application built on:
- [Node.js](https://nodejs.org/)
- [React](https://facebook.github.io/react/)
- [Webpack](http://webpack.github.io/)
- [Metronic](https://keenthemes.com/metronic/) template

### Requirements

- make sure you have the correct [Node.js](https://nodejs.org/) version installed (>= v13.14.0)

### Environment Variables
- `.env.development` - uses on docker
- `.env.development.local` - uses on local development, update REACT_APP_API_BASE_URI depending on the server you need - correct values in `.env.production & .env.staging` (`npm run start`)
- `.env.production`- production environment
- `.env.staging`- staging environment

### Build & Run scripts

    npm install

- to run dev server `npm run start` http://localhost:3000/backend

### Folder structure

```bash
.
├── public
│   ├── css
│   ├── media # metronic assets - feel free to remove unused
│   └── index.html
├── src
│   ├── app
│   │   ├── App.js
│   │   ├── BasePage.js
│   │   ├── common
│   │   │   ├── ... # common custom components
│   │   │   ├── hooks.js # PAY ATTENTION: custom necessary hooks
│   │   │   └── utils.js
│   │   ├── modules # pages of general routing
│   │   │   ├── Auth
│   │   │   │   ├── pages # pages of Auth module
│   │   │   │   └── _redux # redux state of Auth module
│   │   │   ├── DocumentInfo
│   │   │   │   ├── pages
│   │   │   │   │   ├── document
│   │   │   │   │   └── DocumentRoutes.js
│   │   │   │   └── _redux
│   │   │   │       └── document
│   │   │   ├── ErrorsExamples # metronic error templates, probably could be removed
│   │   │   ├── LimitInfo
│   │   │   │   ├── LimitRoutes.js
│   │   │   │   ├── pages
│   │   │   │   │   ├── exemption
│   │   │   │   │   │   ├── components
│   │   │   │   │   │   └── ExemptionPage.js
│   │   │   │   │   └── limit
│   │   │   │   │       ├── components
│   │   │   │   │       └── LimitPage.js
│   │   │   │   └── _redux
│   │   │   │       ├── exemption
│   │   │   │       ├── filters
│   │   │   │       └── limit
│   │   │   ├── NewsInfo
│   │   │   │   ├── pages
│   │   │   │   │   ├── impact-assessment
│   │   │   │   │   ├── news
│   │   │   │   │   ├── source
│   │   │   │   │   └── NewsRoutes.js
│   │   │   │   └── _redux
│   │   │   │       ├── impact-assessment
│   │   │   │       ├── news
│   │   │   │       └── source
│   │   │   ├── OrganizationInfo
│   │   │   │   ├── pages
│   │   │   │   │   ├── organization
│   │   │   │   │   ├── users
│   │   │   │   │   └── OrganizationRoutes.js
│   │   │   │   └── _redux
│   │   │   │       ├── organization
│   │   │   │       └── users
│   │   │   ├── ProductInfo
│   │   │   │   ├── pages
│   │   │   │   │   ├── industry
│   │   │   │   │   ├── material-category
│   │   │   │   │   ├── product-category
│   │   │   │   │   └── ProductRoutes.js
│   │   │   │   └── _redux
│   │   │   │       ├── industry
│   │   │   │       ├── material-category
│   │   │   │       └── product-category
│   │   │   ├── RegionInfo
│   │   │   │   ├── pages
│   │   │   │   │   ├── region-page
│   │   │   │   │   └── RegionRoutes.js
│   │   │   │   └── _redux
│   │   │   │       └── region-page
│   │   │   ├── RegulationInfo
│   │   │   │   ├── pages
│   │   │   │   │   ├── impact-assessment
│   │   │   │   │   ├── issuingbody
│   │   │   │   │   ├── regulations
│   │   │   │   │   ├── regulatory-framework
│   │   │   │   │   └── RegulationRoutes.js
│   │   │   │   └── _redux
│   │   │   │       ├── impact-assessment
│   │   │   │       ├── issuingbody
│   │   │   │       ├── regulation
│   │   │   │       └── regulatory-framework
│   │   │   └── SubstanceInfo
│   │   │       ├── pages
│   │   │       │   ├── family
│   │   │       │   └── substance-data
│   │   │       ├── _redux
│   │   │       │   ├── family
│   │   │       │   └── substance-data
│   │   │       └── SubstanceRoutes.js
│   │   ├── pages
│   │   │   └── DashboardPage.js # metronic empty dashboard page
│   │   └── Routes.js
│   ├── index.js
│   ├── index.scss
│   ├── _metronic # metronic template
│   │   ├── _assets
│   │   ├── _helpers
│   │   ├── i18n
│   │   ├── layout
│   │   └── _partials
│   ├── redux
│   │   ├── app # common app redux
│   │   ├── substances # common substances redux
│   │   ├── commonApiService.js
│   │   ├── index.js
│   │   ├── rootReducer.js
│   │   ├── setupAxios.js
│   │   └── store.js
│   └── static
├── views
├── .env.development
├── .env.development.local
├── .env.production
├── .env.staging
├── admin.py
├── apps.py
├── config-overrides.js
├── __init__.py
├── MANUAL.md
├── package.json
├── package-lock.json
├── serve.json
├── tests.py
├── urls.py
└── webpack.config.js
```

### Possible App Improvements

- [ ] Remove Metric Template
- [ ] Replace webpack builder by [vite](https://vitejs.dev/)
  - [ ] TypeScript
- [ ] Assemble custom ui kit
- [ ] Replace Redux Tool Kit by [React-Query](https://tanstack.com/query/latest/docs/react/adapters/react-query) *(keep the RTK in case to use the global state)*

### Please keep this manual updated


Feel free to contact for any questions about application [nagaev\@digitalaware.dev](mailto:nagaev@digitalaware.dev?subject=RTT)
