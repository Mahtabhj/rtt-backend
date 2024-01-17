import { createSlice } from "@reduxjs/toolkit";

// TODO: move impactAssessment to regulationInfo.impactAssessment
const initialImpactAssessmentState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  impactAssessmentAnswers: null,
  impactAssessmentForEdit: undefined,
  impactAssessmentForSelect: undefined,
  lastError: null,
};

export const callTypes = {
  list: "list",
  action: "action",
};

export const impactAssessmentSlice = createSlice({
  name: "impactAssessment",
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
        state.impactAssessmentForSelect =
          initialImpactAssessmentState.impactAssessmentForSelect;
      } else {
        state.actionsLoading = true;
        state.impactAssessmentForSelect =
          initialImpactAssessmentState.impactAssessmentForSelect;
      }
    },

    //Impact Assessments table

    //list fetched

    impactAssessmentListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
    },

    impactAssessmentAnswersFetched: (state, action) => {
      state.actionsLoading = false;
      state.impactAssessmentAnswers = action.payload.answers;
      state.error = null;
    },

    //updated answers
    impactAssessmentAnswersUpdated: (state, action) => {
      let { currentAns, selectedQuestionsId, impactAssessmentId } = action.payload
      state.actionsLoading = false;
      let newAns = 0;
      let data = currentAns.map(ca => {
        let ans = state.impactAssessmentAnswers.find(x => x.id === ca.id);
        if(!ans) newAns++;
        return { ...ans, ...ca };
      });

      state.impactAssessmentAnswers = [...data];
      state.entities[impactAssessmentId].questions[selectedQuestionsId].answered = 
          newAns === 0 ? 
            state.entities[impactAssessmentId].questions[selectedQuestionsId].answered 
            : state.entities[impactAssessmentId].questions[selectedQuestionsId].answered + newAns;
      
      state.error = null;
    },
    
    userListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.userList = entities;
      state.totalCount = totalCount;
    },
  },
});
