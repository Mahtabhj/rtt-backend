import { createSlice } from "@reduxjs/toolkit";

const initialIssuingBodyState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  issuingbodyForEdit: undefined,
  issuingbodyForSelect: undefined,
  lastError: null,
};

export const callTypes = {
  list: "list",
  action: "action",
};

export const issuingbodySlice = createSlice({
  name: "issuingbody",
  initialState: initialIssuingBodyState,
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
        state.issuingbodyForSelect =
          initialIssuingBodyState.issuingbodyForSelect;
      } else {
        state.actionsLoading = true;
        state.issuingbodyForSelect =
          initialIssuingBodyState.issuingbodyForSelect;
      }
    },

    // getIssuingBodyById
    issuingbodyFetched: (state, action) => {
      state.actionsLoading = false;
      state.issuingbodyForEdit = action.payload.issuingbodyForEdit;
      state.error = null;
    },
    regionListFetched: (state, action) => {
      state.actionsLoading = false;
      state.regionList = action.payload.regionList;
      state.error = null;
    },

    // getIssuingBodyById
    issuingbodySelected: (state, action) => {
      state.actionsLoading = false;
      state.issuingbodyForSelect = action.payload.issuingbodyForSelect;
      state.error = null;
    },

    // getIssuingBodyList
    issuingbodyListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
    },

    // createIssuingBody
    issuingbodyCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.entities.push(action.payload.issuingbody);
    },

    // updateIssuingBody
    issuingbodyUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.map((entity) => {
        if (entity.id === action.payload.issuingbody.id) {
          return action.payload.issuingbody;
        }
        return entity;
      });
    },

    // deleteIssuingBody
    issuingbodyDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(
        (el) => el.id !== action.payload.id
      );
    },

    // issuingbodyUpdateState
    issuingbodyStatusUpdated: (state, action) => {
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

    urlListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.urlList = entities;
      state.totalCount = totalCount;
    },

  },
});
