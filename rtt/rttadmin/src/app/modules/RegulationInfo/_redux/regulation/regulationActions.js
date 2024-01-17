import * as regulationApiService from "./regulationApiService";
import { callTypes, regulationSlice } from "./regulationSlice";
import * as commonApiService from "@redux/commonApiService";

const { actions } = regulationSlice;

export const fetchRegulationList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getRegulationList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.regulationListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulation";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const dropRegulationForEdit = () =>
  dispatch => {
    return dispatch(actions.regulationFetched({ regulationForEdit: null }));
};

export const fetchRegulation = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.regulationFetched({ regulationForEdit: null })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .getRegulationById(id)
    .then((response) => {
      const regulation = response.data;
      dispatch(actions.regulationFetched({ regulationForEdit: regulation }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const selectRegulation = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.regulationSelected({ regulationForSelect: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .getRegulationById(id)
    .then((response) => {
      const regulation = response.data;
      dispatch(actions.regulationSelected({ regulationForSelect: regulation }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteRegulation = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .deleteRegulation(id)
    .then((response) => {
      dispatch(actions.regulationDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createRegulation = (regulationForCreation) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .createRegulation(regulationForCreation)
    .then((response) => {
      const regulation = response.data;
      dispatch(actions.regulationCreated({ regulation }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateRegulation = (regulation) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .updateRegulation(regulation)
    .then(() => {
      dispatch(actions.regulationUpdated({ regulation }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateRegulationField = (regulation) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));

  return regulationApiService
    .updateRegulationField(regulation)
    .then(() => {
      if (!!regulation?.urls?.length) {
        dispatch(actions.regulationUrlsLink({ regulation }));
      }

      if (!!regulation?.documents?.length) {
        dispatch(actions.regulationDocumentsLink({ regulation }));
      }
    })
    .catch((error) => {
      error.clientMessage = "Can't update regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateRegulationStatus = (ids, status) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .updateStatusForRegulation(ids, status)
    .then(() => {
      dispatch(actions.regulationStatusUpdated({ ids, status }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update regulation status";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchUserList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
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

export const fetchTopicList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getAllTopicsList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.topicListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't fetch topic list";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchMaterialCategoryList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getMaterialCategoriesList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.materialCategoriesListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchProductCategoryList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getProductCategoriesList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.productCategoriesListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchDocumentsList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));

  return regulationApiService
    .getDocumentsList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.documentListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchURLsList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getURLsList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.urlListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchRegulationTypeList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getRegulationTypeList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.regulationTypeFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchStatusList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getStatusList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.statusFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchLanguageList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getLanguageList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.languageFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchRegulatoryFrameworkList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getRegulatoryFrameworkList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.regulatoryFrameworkFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

//Related URLs table

//create
export const createRegulationUrl = ({ url, regulationId }) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .createRegulationUrl(url)
    .then((response) => {
      const url = response.data;

      // Update regulation after adding new related url
      return commonApiService
        .getRegulationDetailById(regulationId)
        .then((res) => {
          const relatedRegulation = res.data;
          return regulationApiService
            .updateRegulation({
              ...relatedRegulation,
              urls: [...relatedRegulation.urls, url.id],
            })
            .then((res) => {
              dispatch(actions.regulationUrlCreated({ url }));
            });
        });
    })
    .catch((error) => {
      error.clientMessage = "Can't create link";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//update
export const updateRegulationUrl = (url) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .updateRegulationUrl(url)
    .then(() => {
      dispatch(actions.regulationUrlUpdated({ url }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update url";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Delete
export const deleteUrl = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .deleteUrl(id)
    .then((response) => {
      dispatch(actions.UrlDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete url";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Related attachments or documents table

//Create
export const createRegulationRelatedDocument = ({
  document,
  regulationId,
  typeName,
}) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .createRegulationRelatedDocument(document)
    .then((response) => {
      const document = response.data;

      // Update regulation after adding new related document
      return commonApiService
        .getRegulationDetailById(regulationId)
        .then((res) => {
          let relatedRegulation = res.data;
          return regulationApiService
            .updateRegulation({
              ...relatedRegulation,
              documents: [...relatedRegulation.documents, document.id],
            })
            .then((res) => {
              dispatch(
                actions.regulationDocumentCreated({ document, typeName })
              );
            });
        });
    })
    .catch((error) => {
      error.clientMessage = "Can't create attachment";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Update
export const updateRegulationRelatedDocument = (value) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .updateRegulationRelatedDocument(value.document)
    .then((response) => {
      let data = response.data;
      dispatch(
        actions.regulationDocumentUpdated({
          data: data,
          typeName: value.typeName,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't update related document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Delete
export const deleteDocuments = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .deleteDocuments(id)
    .then((response) => {
      dispatch(actions.documentsDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete url";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Impact Assessment table
export const fetchRegulationImpactAssessment = regulationId =>
  dispatch => {
  dispatch(actions.startCall({ callType: callTypes.action }));

  return regulationApiService
    .getRegulationImpactAssessmentById(regulationId)
    .then((response) => {
      const impactAssessment = response.data.data;
      dispatch(
        actions.regulationImpactAssessmentFetched({
          regulationImpactAssessmentForEdit: impactAssessment,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Fetch Impact Assessment Answers
export const fetchRegulationImpactAssessmentAnswers = regulationId =>
  dispatch => {
  dispatch(actions.startCall({ callType: callTypes.action }));

  return regulationApiService
    .getRegulationImpactAssessmentAnswers(regulationId)
    .then((response) => {
      const impactAssessmentAnswers = response.data.results;
      dispatch(
        actions.regulationImpactAssessmentAnswersFetched({
          answers: impactAssessmentAnswers,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//create
export const createRegulationImpactAssessment = ({
  impactAssessment,
  regulationId,
}) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .createRegulationImpactAssessment(impactAssessment)
    .then((response) => {
      // const url = response.data;

      return regulationApiService
        .getRegulationById(regulationId)
        .then((res) => {
          const relatedRegulation = res.data;

          return regulationApiService
            .updateRegulation({ ...relatedRegulation, impactAssessment })
            .then((res) => {
              dispatch(
                actions.regulationImpactAssessmentCreated({ impactAssessment })
              );
            });
        });
    })
    .catch((error) => {
      error.clientMessage = "Can't create ImpactAssessment";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//update
export const updateRegulationImpactAssessment = (url) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .updateRegulationImpactAssessment(url)
    .then(() => {
      dispatch(actions.regulationImpactAssessmentUpdated({ url }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update ImpactAssessment";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Delete
export const deleteImpactAssessment = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .deleteImpactAssessment(id)
    .then((response) => {
      dispatch(actions.ImpactAssessmentDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete ImpactAssessment";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//update answers

export const updateRegulationImpactAssessmentAnswers = ({
  answers,
  selectedQuestionsId,
}) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  let currentAns = [];
  answers.map((ans) => {
    return regulationApiService
      .updateImpactAssessmentAnswers(ans)
      .then((res) => {
        let ca = res.data;
        currentAns.push(ca);
        if (currentAns.length === answers.length)
          dispatch(
            actions.regulationImpactAssessmentAnswersUpdated({
              currentAns,
              selectedQuestionsId,
            })
          );
      });
  });
};

// Related milestone table

export const fetchRelatedMilestoneList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getRelatedMilestoneList(queryParams)
    .then((response) => {
      const totalCount = response.count;
      const entities = response.data.results;
      dispatch(
        actions.relatedMilestoneListFetched({
          totalCount,
          entities,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find related Milestone";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchMilestoneTypeList = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulationApiService
    .getMilestoneTypeList()
    .then((response) => {
      const totalCount = 0;
      const entities = response.data.results;
      dispatch(
        actions.milestoneTypeListFetched({
          totalCount,
          entities,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find milestone type list";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const createRelatedMilestone = (milestone) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .createRelatedMilestone(milestone)
    .then((response) => {
      const milestone = response.data;
      dispatch(actions.relatedMilestoneCreated({ milestone }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create Milestone";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateRelatedMilestone = (milestone) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .updateRelatedMilestone(milestone)
    .then(() => {
      dispatch(actions.relatedMilestoneUpdated({ milestone }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update related milestone";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteRelatedMilestone = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .deleteRelatedMilestone(id)
    .then((response) => {
      dispatch(actions.relatedMilestoneDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete milestone";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchRelatedMilestone = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.relatedMilestoneFetched({
        relatedMilestoneForEdit: undefined,
      })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .getRelatedMilestoneById(id)
    .then((response) => {
      const data = response.data;
      dispatch(
        actions.relatedMilestoneFetched({
          relatedMilestoneForEdit: data,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find Milestone";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createMilestoneUrl = (url, setEmptyMilestone, emptyMilestone) => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .createRegulationUrl(url)
    .then((response) => {
      const url = response.data;
      // setEmptyMilestone({
      //   ...emptyMilestone,
      //   urls: [...emptyMilestone.urls, url],
      // });
      dispatch(actions.milestoneUrlCreated({ url }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create Milestone Url";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateMilestoneUrl = (url) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .updateRegulationUrl(url)
    .then((response) => {
      const url = response.data;
      dispatch(actions.milestoneUrlUpdated({ url }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update Milestone Url";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const milestoneDropLastAttachmentsAction = () => (dispatch) => {
  dispatch(actions.milestoneDropLastAttachments());
};

export const createMilestoneDocument = (
  document,
  setEmptyMilestone,
  emptyMilestone
) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .createRegulationRelatedDocument(document)
    .then((response) => {
      const document = response.data;
      // setEmptyMilestone({
      //   ...emptyMilestone,
      //   documents: [...emptyMilestone.documents, document],
      // });
      dispatch(actions.milestoneDocumentCreated({ document }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create Milestone Docuemts";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateMilestoneDocument = (document) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulationApiService
    .updateRegulationRelatedDocument(document)
    .then((response) => {
      const document = response.data;
      dispatch(actions.milestoneDocumentUpdated({ document }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update Milestone Document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};