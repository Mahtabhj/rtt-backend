import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  relatedSubstances: { count: 0, results: [] },
  entityQuery: null,
};

export const callTypes = {
  list: "list",
  action: "action",
};

export const substancesSlice = createSlice({
  name: "substances",
  initialState,
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
      } else {
        state.actionsLoading = true;
      }
    },

    relatedSubstancesFetched: (state, action) => {
      const { count, results, entityQuery } = action.payload;

      state.listLoading = false;
      state.error = null;
      state.relatedSubstances = { count, results };
      state.entityQuery = entityQuery;
    },

    substancesAddedManual: (state) => {
      state.actionsLoading = false;
      state.error = null;
    },

    substancesUploaded: (state) => {
      state.actionsLoading = false;
      state.error = null;
    },
  },
});
