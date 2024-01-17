import * as regulatoryFrameworkApiService from "./regulatoryFrameworkApiService";
import {
  regulatoryFrameworkSlice,
  callTypes,
} from "./regulatoryFrameworkSlice";
import * as commonApiService from "@redux/commonApiService";

const { actions } = regulatoryFrameworkSlice;

export const fetchRegulatoryFrameworkList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
    .getRegulatoryFrameworkList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(
        actions.regulatoryFrameworkListFetched({ totalCount, entities })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulatoryFramework";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchTopicList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
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

export const fetchRegulatoryFramework = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.regulatoryFrameworkFetched({
        regulatoryFrameworkForEdit: undefined,
      })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .getRegulatoryFrameworkById(id)
    .then((response) => {
      const regulatoryFramework = response.data;
      dispatch(
        actions.regulatoryFrameworkFetched({
          regulatoryFrameworkForEdit: regulatoryFramework,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulatoryFramework";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const selectRegulatoryFramework = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.regulatoryFrameworkSelected({
        regulatoryFrameworkForSelect: undefined,
      })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .getRegulatoryFrameworkById(id)
    .then((response) => {
      const regulatoryFramework = response.data;
      dispatch(
        actions.regulatoryFrameworkSelected({
          regulatoryFrameworkForSelect: regulatoryFramework,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulatoryFramework";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteRegulatoryFramework = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .deleteRegulatoryFramework(id)
    .then((response) => {
      dispatch(actions.regulatoryFrameworkDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete regulatoryFramework";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createRegulatoryFramework = regulatoryFrameworkForCreation => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .createRegulatoryFramework(regulatoryFrameworkForCreation)
    .then((response) => {
      const regulatoryFramework = response.data;
      dispatch(actions.regulatoryFrameworkCreated({ regulatoryFramework }));

      return regulatoryFramework.id;
    })
    .catch((error) => {
      error.clientMessage = "Can't create regulatoryFramework";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateRegulatoryFramework = (regulatoryFramework) => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .updateRegulatoryFramework(regulatoryFramework)
    .then((response) => {
      dispatch(actions.regulatoryFrameworkUpdated({ regulatoryFramework }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update regulatory framework";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateRegulatoryFrameworkField = (regulatoryFramework) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));

  return regulatoryFrameworkApiService
    .updateRegulatoryFrameworkField(regulatoryFramework)
    .then(() => {
      if (!!regulatoryFramework?.urls?.length) {
        dispatch(actions.regulatoryFrameworkUrlsLink({ regulatoryFramework }));
      }

      if (!!regulatoryFramework?.documents?.length) {
        dispatch(actions.regulatoryFrameworkDocumentsLink({ regulatoryFramework }));
      }
    })
    .catch((error) => {
      error.clientMessage = "Can't update regulatory framework";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateRegulatoryFrameworkStatus = (ids, status) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .updateStatusForRegulatoryFramework(ids, status)
    .then(() => {
      dispatch(actions.regulatoryFrameworkStatusUpdated({ ids, status }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update regulatoryFramework status";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchRelatedRegulationList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
    .getRelatedRegulationList(queryParams)
    .then((response) => {
      const totalCount = response.count;
      const entities = response.data.results;
      dispatch(
        actions.regulatoryFrameworkRelatedRegulationListFetched({
          totalCount,
          entities,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find related regulation";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const milestoneDropLastAttachmentsAction = () => (dispatch) => {
  dispatch(actions.milestoneDropLastAttachments());
};

export const fetchRegulatoryFrameworkSelectedRegulation = (id) => (
  dispatch
) => {
  if (!id) {
    return dispatch(
      actions.regulatoryFrameworkRelatedRegulationFetched({
        regulatoryFrameworkRelatedRegulationForEdit: undefined,
      })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return commonApiService
    .getRegulationDetailById(id)
    .then((response) => {
      const data = response.data;
      dispatch(
        actions.regulatoryFrameworkRelatedRegulationFetched({
          regulatoryFrameworkRelatedRegulationForEdit: data,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createRegulatoryFrameworkRelatedRegulation = (regulation) => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .createRegulatoryFrameworkRelatedRegulation(regulation)
    .then((response) => {
      const regulation = response.data;
      dispatch(
        actions.regulatoryFrameworkRelatedRegulationCreated({ regulation })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't create organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createRegulatoryFrameworkLink = (link) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .createRegulatoryFrameworkLink(link)
    .then((response) => {
      const link = response.data;
      dispatch(actions.regulatoryFrameworkLinkCreated({ link }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create link";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateRegulatoryFrameworkLink = (link) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .updateRegulatoryFrameworkLink(link)
    .then(() => {
      dispatch(actions.regulatoryFrameworkLinkUpdated({ link }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update related regulation";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteRegulatoryFrameworkRelatedRegulation = (id) => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .deleteRegulatoryFrameworkRelatedRegulation(id)
    .then((response) => {
      dispatch(actions.regulatoryFrameworkRelatedRegulationDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteLink = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .deleteLink(id)
    .then((response) => {
      dispatch(actions.linkDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

// Related Milestones Actions

export const fetchRelatedMilestoneList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
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

export const fetchRelatedMilestone = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.relatedMilestoneFetched({
        relatedMilestoneForEdit: undefined,
      })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
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

export const createRelatedMilestone = (milestone) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
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
  return regulatoryFrameworkApiService
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
  return regulatoryFrameworkApiService
    .deleteRelatedMilestone(id)
    .then((response) => {
      dispatch(actions.relatedMilestoneDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete milestone";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchLanguageList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
    .getLanguageList(queryParams)
    .then((response) => {
      const totalCount = response.count;
      const entities = response.data.results;
      dispatch(
        actions.languageListFetched({
          totalCount,
          entities,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find Language list";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchStatusList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
    .getStatusList(queryParams)
    .then((response) => {
      const totalCount = response.count;
      const entities = response.data.results;
      dispatch(
        actions.statusListFetched({
          totalCount,
          entities,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find Language list";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchRegulationTypeList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
    .getRegulationTypeList(queryParams)
    .then((response) => {
      const totalCount = response.count;
      const entities = response.data.results;
      dispatch(
        actions.regulationTypeListFetched({
          totalCount,
          entities,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find Issue list";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchUserList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
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

export const fetchMaterialCategoryList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
    .getMaterialCategoryList(queryParams)
    .then((response) => {
      const totalCount = response.count;
      const entities = response.data.results;
      dispatch(
        actions.materialCategoryListFetched({
          totalCount,
          entities,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find material category list";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchProductCategoryList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
    .getProductCategoryList(queryParams)
    .then((response) => {
      const totalCount = response.count;
      const entities = response.data.results;
      dispatch(
        actions.productCategoryListFetched({
          totalCount,
          entities,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find product category list";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchLinkList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
    .getLinkList(queryParams)
    .then((response) => {
      const totalCount = response.count;
      const entities = response.data.results;
      dispatch(
        actions.linkListFetched({
          totalCount,
          entities,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find link list";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchMilestoneTypeList = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
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

//Impact Assessment table

export const fetchRegulatoryFrameworkImpactAssessment = (
  regulatoryFrameworkId
) => (dispatch) => {
  if (!regulatoryFrameworkId) {
    return dispatch(
      actions.regulatoryFrameworkImpactAssessmentFetched({
        regulatoryFrameworkImpactAssessmentForEdit: undefined,
      })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.aregulationIdction }));
  return regulatoryFrameworkApiService
    .getRegulatoryFrameworkImpactAssessmentById(regulatoryFrameworkId)
    .then((response) => {
      const impactAssessment = response.data.data;
      dispatch(
        actions.regulatoryFrameworkImpactAssessmentFetched({
          regulatoryFrameworkImpactAssessmentForEdit: impactAssessment,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulatoryFramework";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Fetch Impact Assessment Answers

export const fetchRegulatoryFrameworkImpactAssessmentAnswers = (rfId) => (
  dispatch
) => {
  // if (!regulatoryFrameworkId) {
  //   return dispatch(
  //     actions.regulatoryFrameworkImpactAssessmentFetched({ regulatoryFrameworkImpactAssessmentForEdit: undefined })
  //   );
  // }

  dispatch(actions.startCall({ callType: callTypes.aregulationIdction }));
  return regulatoryFrameworkApiService
    .getRegulatoryFrameworkImpactAssessmentAnswers(rfId)
    .then((response) => {
      const impactAssessmentAnswers = response.data.results;
      dispatch(
        actions.regulatoryFrameworkImpactAssessmentAnswersFetched({
          answers: impactAssessmentAnswers,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find regulatoryFramework";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//create
export const createRegulatoryFrameworkImpactAssessment = ({
  impactAssessment,
  regulatoryFrameworkId,
}) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .createRegulatoryFrameworkImpactAssessment(impactAssessment)
    .then((response) => {
      return regulatoryFrameworkApiService
        .getRegulatoryFrameworkById(regulatoryFrameworkId)
        .then((res) => {
          const relatedRegulatoryFramework = res.data;

          return regulatoryFrameworkApiService
            .updateRegulatoryFramework({
              ...relatedRegulatoryFramework,
              impactAssessment,
            })
            .then((res) => {
              dispatch(
                actions.regulatoryFrameworkImpactAssessmentCreated({
                  impactAssessment,
                })
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
export const updateRegulatoryFrameworkImpactAssessment = (url) => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .updateRegulatoryFrameworkImpactAssessment(url)
    .then(() => {
      dispatch(actions.regulatoryFrameworkImpactAssessmentUpdated({ url }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update ImpactAssessment";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Delete
export const deleteImpactAssessment = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
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

export const updateRegulatoryFrameworkImpactAssessmentAnswers = ({
  answers,
  selectedQuestionsId,
}) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  let currentAns = [];
  answers.map((ans) => {
    return regulatoryFrameworkApiService
      .updateImpactAssessmentAnswers(ans)
      .then((res) => {
        let ca = res.data;
        currentAns.push(ca);
        if (currentAns.length === answers.length)
          dispatch(
            actions.regulatoryFrameworkImpactAssessmentAnswersUpdated({
              currentAns,
              selectedQuestionsId,
            })
          );
      });
  });
};

//Related attachments or documents table

//Create
export const createRegulatoryFrameworkRelatedDocument = ({
  document,
  regulatoryFrameworkId,
}) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .createRegulatoryFrameworkRelatedDocument(document)
    .then((response) => {
      const document = response.data;

      return regulatoryFrameworkApiService
        .getRegulatoryFrameworkById(regulatoryFrameworkId)
        .then((res) => {
          const relatedRegulatoryFramework = res.data;

          let newDoc = {
            id: response.data.id,
            title: response.data.title,
            attachment: response.data.attachment,
          };

          let docIds = [newDoc.id];

          relatedRegulatoryFramework.documents.map((d) => {
            return docIds.push(d.id);
          });

          return regulatoryFrameworkApiService
            .updateRegulatoryFrameworkDocuments({
              regulatoryFrameworkId: relatedRegulatoryFramework.id,
              documents: docIds,
            })
            .then((res) => {
              dispatch(
                actions.regulatoryFrameworkDocumentCreated({ document })
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
export const updateRegulatoryFrameworkRelatedDocument = (document) => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .updateRegulatoryFrameworkRelatedDocument(document)
    .then(() => {
      dispatch(actions.regulatoryFrameworkDocumentUpdated({ document }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update related document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Delete
export const deleteDocuments = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .deleteDocuments(id)
    .then((response) => {
      dispatch(actions.documentsDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete url";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createMilestoneUrl = (url, setEmptyMilestone, emptyMilestone) => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .createUrl(url)
    .then((response) => {
      const url = response.data;
      // setEmptyMilestone({
      //   ...emptyMilestone,
      //   urls: [...emptyMilestone.urls, url],
      // });
      dispatch(actions.urlCreated({ url }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create Milestone Url";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateMilestoneUrl = (url) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .updateUrl(url)
    .then((response) => {
      const url = response.data;
      dispatch(actions.urlUpdated({ url }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update Milestone Url";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createMilestoneDocument = (
  document,
  setEmptyMilestone,
  emptyMilestone
) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .createRegulatoryFrameworkRelatedDocument(document)
    .then((response) => {
      const document = response.data;
      // setEmptyMilestone({
      //   ...emptyMilestone,
      //   documents: [...emptyMilestone.documents, document],
      // });
      dispatch(actions.documentCreated({ document }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create Milestone Document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateMilestoneDocument = (document) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return regulatoryFrameworkApiService
    .updateRegulatoryFrameworkRelatedDocument(document)
    .then((response) => {
      const document = response.data;
      dispatch(actions.documentUpdated({ document }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update Milestone Document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchDocumentsList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return regulatoryFrameworkApiService
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
