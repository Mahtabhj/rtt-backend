import * as impactAssessmentApiService from "./impactAssessmentApiService";
import { impactAssessmentSlice, callTypes } from "./impactAssessmentSlice";

const { actions } = impactAssessmentSlice;

export const fetchImpactAssessmentList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return impactAssessmentApiService
    .getImpactAssessmentList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.impactAssessmentListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find Impact Assessment";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchImpactAssessmentAnswers = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.aregulationIdction }));
  return impactAssessmentApiService
    .getImpactAssessmentAnswers()
    .then((response) => {
      const impactAssessmentAnswers = response.data.results;
      dispatch(
        actions.impactAssessmentAnswersFetched({
          answers: impactAssessmentAnswers,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//update answers
export const updateImpactAssessmentAnswers = ({
  answers,
  selectedQuestionsId,
  impactAssessmentId,
}) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  let currentAns = [];
  answers.map((ans) => {
    return impactAssessmentApiService
      .updateImpactAssessmentAnswers(ans)
      .then((res) => {
        let ca = res.data;
        currentAns.push(ca);
        if (currentAns.length === answers.length)
          dispatch(
            actions.impactAssessmentAnswersUpdated({
              currentAns,
              selectedQuestionsId,
              impactAssessmentId,
            })
          );
      });
  });
};

export const fetchUserList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return impactAssessmentApiService
    .getUserList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.userListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};
