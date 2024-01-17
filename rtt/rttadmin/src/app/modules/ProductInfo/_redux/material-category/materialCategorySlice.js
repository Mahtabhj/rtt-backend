import {createSlice} from "@reduxjs/toolkit";

const initialMaterialCategoryState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  materialCategoryForEdit: undefined,
  lastError: null,
  success: false,
};

export const callTypes = {
  list: "list",
  action: "action"
};

export const materialCategorySlice = createSlice({
  name: "materialCategory",
  initialState: initialMaterialCategoryState,
  reducers: {

    catchError: (state, action) => {
      state.success = false;
      state.error = `${action.type}: ${action.payload.error}`;
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
        state.materialCategoryForSelect = initialMaterialCategoryState.materialCategoryForSelect
      } else {
        state.actionsLoading = true;
        state.materialCategoryForSelect = initialMaterialCategoryState.materialCategoryForSelect
      }
    },

    // getMaterialCategoryById
    materialCategoryFetched: (state, action) => {
      state.actionsLoading = false;
      state.materialCategoryForEdit = action.payload.materialCategoryForEdit;
      state.error = null;
    },

    // getMaterialCategoryList
    materialCategoryListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
    },

    // createMaterialCategory
    materialCategoryCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.success = true;
      state.entities.push(action.payload.materialCategory);
    },

    // updateMaterialCategory
    materialCategoryUpdated: (state, action) => {
      state.error = null;
      state.success = true;
      state.actionsLoading = false;
      state.entities = state.entities.map(entity => {
        if (entity.id === action.payload.materialCategory.id) {
          return action.payload.materialCategory;
        }
        return entity;
      });
    },

    // deleteMaterialCategory
    materialCategoryDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(el => el.id !== action.payload.id);
    },

  }
});
