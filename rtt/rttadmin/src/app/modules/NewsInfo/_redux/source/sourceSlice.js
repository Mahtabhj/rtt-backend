import { createSlice } from "@reduxjs/toolkit";

const initialSourceState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  sourceForEdit: undefined,
  sourceForSelect: undefined,
  sourceType: undefined,
  lastError: null,
};

export const callTypes = {
  list: "list",
  action: "action",
};

export const sourceSlice = createSlice({
  name: "source",
  initialState: initialSourceState,
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
        state.sourceForSelect = initialSourceState.sourceForSelect;
      } else {
        state.actionsLoading = true;
        state.sourceForSelect = initialSourceState.sourceForSelect;
      }
    },

    // getSourceById
    sourceFetched: (state, action) => {
      state.actionsLoading = false;
      state.sourceForEdit = action.payload.sourceForEdit;
      state.error = null;
    },

    // getSourceById
    sourceSelected: (state, action) => {
      state.actionsLoading = false;
      state.sourceForSelect = action.payload.sourceForSelect;
      state.error = null;
    },

    // getSourceList
    sourceListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
    },
    sourceTypeListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.sourceType = entities;
      state.totalCount = totalCount;
    },

    // createSource
    sourceCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.entities.push(action.payload.source);
    },

    // updateSource
    sourceUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.map((entity) => {
        if (entity.id === action.payload.source.id) {
          return action.payload.source;
        }
        return entity;
      });
    },

    // deleteSource
    sourceDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(
        (el) => el.id !== action.payload.id
      );
    },

    // sourceUpdateState
    sourceStatusUpdated: (state, action) => {
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
  },
});
