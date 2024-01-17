import { createSlice } from "@reduxjs/toolkit";

const initialDocumentState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  documentForEdit: undefined,
  documentForSelect: undefined,
  lastError: null,
};

export const callTypes = {
  list: "list",
  action: "action",
};

export const documentSlice = createSlice({
  name: "document",
  initialState: initialDocumentState,
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
        state.documentForSelect = initialDocumentState.documentForSelect;
      } else {
        state.actionsLoading = true;
        state.documentForSelect = initialDocumentState.documentForSelect;
      }
    },

    // getDocumentById
    documentFetched: (state, action) => {
      state.actionsLoading = false;
      state.documentForEdit = action.payload.documentForEdit;
      state.error = null;
    },

    // getDocumentById
    documentSelected: (state, action) => {
      state.actionsLoading = false;
      state.documentForSelect = action.payload.documentForSelect;
      state.error = null;
    },

    // getDocumentList
    documentListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
    },

    documentTypeListFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.documentTypeList = entities;
    },
    // createDocument
    documentCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.entities.push(action.payload.document);
    },

    // updateDocument
    documentUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.map((entity) => {
        if (entity.id === action.payload.document.id) {
          return action.payload.document;
        }
        return entity;
      });
    },

    // deleteDocument
    documentDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(
        (el) => el.id !== action.payload.id
      );
    },

    // documentUpdateState
    documentStatusUpdated: (state, action) => {
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
