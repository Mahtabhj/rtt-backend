import {createSlice} from "@reduxjs/toolkit";

const initialProductCategoryState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  productCategoryForEdit: undefined,
  lastError: null
};

export const callTypes = {
  list: "list",
  action: "action"
};

export const productCategorySlice = createSlice({
  name: "productCategory",
  initialState: initialProductCategoryState,
  reducers: {

    catchError: (state, action) => {
      state.error = `${action.type}: ${action.payload.error}`;
      if (action.payload.callType === callTypes.list) {
        state.listLoading = false;
      } else {
        state.actionsLoading = false;
      }
    },

    startCall: (state, action) => {
      state.error = null;
      if (action.payload.callType === callTypes.list) {
        state.listLoading = true;
        state.productCategoryForSelect = initialProductCategoryState.productCategoryForSelect
      } else {
        state.actionsLoading = true;
        state.productCategoryForSelect = initialProductCategoryState.productCategoryForSelect
      }
    },

    // getProductCategoryById
    productCategoryFetched: (state, action) => {
      state.actionsLoading = false;
      state.productCategoryForEdit = action.payload.productCategoryForEdit;
      state.error = null;
    },

    // getProductCategoryById
    productCategorySelected: (state, action) => {
      state.actionsLoading = false;
      state.productCategoryForSelect = action.payload.productCategoryForSelect;
      state.error = null;
    },

    // getProductCategoryList
    productCategoryListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
    },

    // createProductCategory
    productCategoryCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.entities.push(action.payload.productCategory);
    },

    // updateProductCategory
    productCategoryUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.map(entity => {
        if (entity.id === action.payload.productCategory.id) {
          return action.payload.productCategory;
        }
        return entity;
      });
    },

    // deleteProductCategory
    productCategoryDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(el => el.id !== action.payload.id);
    },
    
    // productCategoryUpdateState
    productCategoryStatusUpdated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      const { ids, status } = action.payload;
      state.entities = state.entities.map(entity => {
        if (ids.findIndex(id => id === entity.id) > -1) {
          entity.status = status;
        }
        return entity;
      });
    },

    industryListFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.industryList = entities;
    },
  }
});
