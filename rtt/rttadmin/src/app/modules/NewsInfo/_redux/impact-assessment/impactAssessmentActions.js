import * as impactAssessmentApiService from "./impactAssessmentApiService";
import { newsImpactAssessmentSlice, callTypes } from "./impactAssessmentSlice";
import { toast } from "react-toastify";

const { actions } = newsImpactAssessmentSlice;

export const fetchImpactAssessmentList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return impactAssessmentApiService
    .getImpactAssessmentList(queryParams)
    .then(response => {
      const { count, results } = response.data;
      dispatch(actions.impactAssessmentListFetched({ count, results }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find Impact Assessment";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

// uses news details api
export const selectImpactAssessment = (id) => (dispatch) => {
  if (!id) {
    return dispatch(actions.impactAssessmentSelected({ impactAssessmentForSelect: undefined }));
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return impactAssessmentApiService
    .getImpactAssessmentById(id)
    .then((response) => {
      const impactAssessment = response.data;
      dispatch(actions.impactAssessmentSelected({ impactAssessmentForSelect: impactAssessment }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find Impact Assessment";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchImpactAssessmentQuestions = organizationId => dispatch => {
  dispatch(actions.newsImpactAssessmentQuestionsRequested({}));
  return impactAssessmentApiService
    .getImpactAssessmentQuestions(organizationId)
    .then(response => {
      const questions = response.data.results;
      dispatch(actions.newsImpactAssessmentQuestionsFetched({ questions }));
    })
    .catch(error => {
      error.clientMessage = "Can't find Impact Assessment Questions";
    });
};

export const addImpactAssessmentAnswers = (newsId, dataToSend) => dispatch => {
  dispatch(actions.startCall({ callType: callTypes.action }));

  return impactAssessmentApiService
    .addImpactAssessmentAnswers(newsId, dataToSend)
    .then((response) => {
      toast.success(response.data.message, { position: toast.POSITION.TOP_RIGHT });
      dispatch(actions.answersAdded({}));
    })
    .catch((error) => {
      error.clientMessage = "Can't add answers";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};