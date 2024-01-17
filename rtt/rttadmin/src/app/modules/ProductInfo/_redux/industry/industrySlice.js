import {createSlice} from "@reduxjs/toolkit";

const initialIndustryState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  industryForEdit: undefined,
  lastError: null
};

export const callTypes = {
  list: "list",
  action: "action"
};

export const industrySlice = createSlice({
  name: "industry",
  initialState: initialIndustryState,
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
        state.industryForSelect = initialIndustryState.industryForSelect
      } else {
        state.actionsLoading = true;
        state.industryForSelect = initialIndustryState.industryForSelect
      }
    },

    // getIndustryById
    industryFetched: (state, action) => {
      state.actionsLoading = false;
      state.industryForEdit = action.payload.industryForEdit;
      state.error = null;
    },

    // getIndustryById
    industrySelected: (state, action) => {
      state.actionsLoading = false;
      state.industryForSelect = action.payload.industryForSelect;
      state.error = null;
    },

    // getIndustryList
    industryListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
    },

    // createIndustry
    industryCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.entities.push(action.payload.industry);
    },

    // updateIndustry
    industryUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.map(entity => {
        if (entity.id === action.payload.industry.id) {
          return action.payload.industry;
        }
        return entity;
      });
    },

    // deleteIndustry
    industryDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(el => el.id !== action.payload.id);
    },
    
    // industryUpdateState
    industryStatusUpdated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      const { ids, status } = action.payload;
      state.entities = state.entities.map(entity => {
        if (ids.findIndex(id => id === entity.id) > -1) {
          entity.status = status;
        }
        return entity;
      });
    }
  }
});
