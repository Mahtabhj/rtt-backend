import { createSlice } from "@reduxjs/toolkit";

const initialNewsState = {
  listLoading: false,
  actionsLoading: false,
  reviewCount: 0,
  totalCount: 0,
  entities: null,
  newsForEdit: undefined,
  newsForSelect: undefined,
  lastError: null,
  sourceList: [],
  categoryList: [],
  regulationList: [],
  productCategoryList: [],
  materialCategoryList: [],
  organizationList: [],
  regulationFrameworkList: [],
  documentList: [],
  tab: "new",
  success: false,
  filterOptions: {
    regions: null,
    news_categories: null,
    product_categories: null,
  },
  searchValue: ''
};

export const callTypes = {
  list: "list",
  action: "action",
};

export const newsSlice = createSlice({
  name: "news",
  initialState: initialNewsState,
  reducers: {
    catchError: (state, action) => {
      state.error = `${action.type}: ${action.payload.error}`;
      state.success = false;
      if (action.payload.callType === callTypes.list) {
        state.listLoading = false;
      } else {
        state.actionsLoading = false;
      }
    },

    startCall: (state, action) => {
      state.error = null;
      state.success = false;
      if (action.payload.callType === callTypes.list) {
        state.listLoading = true;
      } else {
        state.actionsLoading = true;
      }
    },

    setTab: (state, action) => {
      state.tab = action.payload;
    },

    // getNewsById
    newsFetched: (state, action) => {
      state.actionsLoading = false;
      state.newsForEdit = action.payload.newsForEdit;
      state.error = null;
    },

    // getNewsById
    newsSelected: (state, action) => {
      state.actionsLoading = false;
      state.newsForSelect = action.payload.newsForSelect;
      state.error = null;
    },

    // getNewsList
    newsListFetched: (state, action) => {
      const { entities, totalCount, reviewCount } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
      state.reviewCount = reviewCount || 0;
    },

    newsRelevanceListFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.newsRelevanceList = entities;
    },

    sourceListFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.sourceList = entities;
    },

    categoryListFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.categoryList = entities;
    },

    regulationListFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.regulationList = entities;
    },

    productCategoryListFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.productCategoryList = entities;
    },

    materialCategoryListFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.materialCategoryList = entities;
    },

    organizationListFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.organizationList = entities;
    },

    regulationFrameworkFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.regulationFrameworkList = entities;
    },

    documentsFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.documentList = entities;
    },

    documentTypeListFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.documentTypeList = entities;
    },

    // createNews
    newsCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.success = 'news';
      // I don't understand why we need it and for what but entities is null
      if (state.entities?.length) {
        state.entities.push(action.payload.news);
      }
    },

    // updateNews
    newsUpdated: (state, action) => {
      state.error = null;
      state.success = 'news';
      state.actionsLoading = false;
      if (state.entities) {
        state.entities = state.entities.map((entity) => {
          if (entity.id === action.payload.news.id) {
            return action.payload.news;
          }
          return entity;
        });
      }
    },

    // selectNewsPatch
    newsPatching: (state) => {
      state.error = null;
      state.actionsLoading = false;
    },

    newsPatched: (state) => {
      state.actionsLoading = false;
      state.error = null;
    },

    newsReviewUpdated: (state, { payload }) => {
      state.actionsLoading = false;
      state.error = null;
      state.entities = state.entities?.map(news => news.id === payload.id ? ({ ...news, ...payload.dataToSend }) : news);
    },

    // deleteNews
    newsDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(
        (el) => el.id !== action.payload.id
      );
    },

    // dischargeNews
    newsDischarged: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(
        (el) => el.id !== action.payload.id
      );
    },

    // newsUpdateState
    newsStatusUpdated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      const { ids, status } = action.payload;
      state.entities = state.entities.map((entity) => {
        if (ids.findIndex((id) => id === entity.id) > -1) {
          entity.status = status;
        }
        return entity;
      });
    },

    //News related documents or attachments

    newsDocumentCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      let newDoc = {
        id: action.payload.document.id,
        title: action.payload.document.title,
        attachment: action.payload.document.attachment,
      };
      state.newsForEdit.documents.push(newDoc);
      state.documentList.push(action.payload.document);
    },

    //update
    newsDocumentUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.newsForEdit.documents = state.newsForEdit.documents.map(
        (entity) => {
          if (entity.id === action.payload.document.id) {
            return action.payload.document;
          }
          return entity;
        }
      );
    },
    //delete
    documentsDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.newsForEdit.documents = state.newsForEdit.documents.filter(
        (doc) => doc !== action.payload.id
      );
    },

    //news impact assessment
    newsRelevanceCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.newsRelevanceList.push(action.payload.relevance);
    },

    newsRelevanceUpdated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.newsRelevanceList = state.newsRelevanceList.map((rel) => {
        if (rel.id === action.payload.relevance.id)
          return action.payload.relevance;
        return rel;
      });
    },

    newsRelevanceDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.newsRelevanceList = state.newsRelevanceList.filter(
        (nr) => nr !== action.payload.id
      );
    },

    regionListFetched: (state, action) => {
      state.actionsLoading = false;
      state.regionList = action.payload.regionList;
      state.error = null;
    },

    newsFromDateSaved: (state) => {
      state.actionsLoading = false;
      state.error = null;
    },

    // filtering
    updateFilter: (state, action) => {
      state.filterOptions = {
        ...state.filterOptions,
        ...action.payload
      };
    },

    applyFilter: (state) => {
      state.isFiltered = true;
    },

    resetFilter: (state) => {
      state.filterOptions = { ...initialNewsState.filterOptions };
      state.isFiltered = false;
    },

    updateSearchValue: (state, action) => {
      state.searchValue = action.payload;
    }
  },
});

export const { setTab, updateFilter, applyFilter, resetFilter, updateSearchValue } = newsSlice.actions;