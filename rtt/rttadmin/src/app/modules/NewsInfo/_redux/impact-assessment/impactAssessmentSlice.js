import { createSlice } from "@reduxjs/toolkit";

const initialImpactAssessmentState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  impactAssessmentForSelect: undefined,
  tab: "to_be_assessed",
  lastError: null,
  questions: [],
};

export const callTypes = {
  list: "list",
  action: "action",
};

export const newsImpactAssessmentSlice = createSlice({
  name: "newsImpactAssessment",
  initialState: initialImpactAssessmentState,
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
        state.impactAssessmentForSelect = initialImpactAssessmentState.impactAssessmentForSelect;
      } else {
        state.actionsLoading = true;
      }
    },

    setTab: (state, action) => {
      state.tab = action.payload;
    },

    //list fetched
    impactAssessmentListFetched: (state, action) => {
      const { count, results } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = results;
      state.totalCount = count;
    },

    // getImpactAssessmentById
    impactAssessmentSelected: (state, action) => {
      state.actionsLoading = false;
      state.impactAssessmentForSelect = action.payload.impactAssessmentForSelect;
      state.error = null;
    },


    newsImpactAssessmentQuestionsRequested: (state) => {
      state.questions = initialImpactAssessmentState.questions;
    },

    newsImpactAssessmentQuestionsFetched: (state, action) => {
      const { questions } = action.payload;
      state.questions = questions;
    },

    answersAdded: (state) => {
      state.actionsLoading = false;
      state.error = null;
    },
  },
});
