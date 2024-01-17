import { createSlice } from "@reduxjs/toolkit";

const initialRegulationState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  regulationForEdit: null,
  regulationForSelect: undefined,
  regulationImpactAssessmentForEdit: undefined,
  impactAssessmentAnswers: undefined,
  lastError: null,
  materialCategoryList: null,
  productCategoryList: null,
  documentList: null,
  userList: null,
  urlList: null,
  success: true,
  lastAddedDocument: null,
  lastAddedUrl: null,
  isFiltered: false,
  filterOptions: {
    regulatory_framework: null,
    type: null,
    review_status: null,
  },
  searchValue: ''
};

export const callTypes = {
  list: "list",
  action: "action",
};

export const regulationSlice = createSlice({
  name: "regulation",
  initialState: initialRegulationState,
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
        state.regulationForSelect = initialRegulationState.regulationForSelect;
      } else {
        state.actionsLoading = true;
        state.regulationForSelect = initialRegulationState.regulationForSelect;
      }
    },

    // getRegulationById
    regulationFetched: (state, action) => {
      state.actionsLoading = false;
      state.regulationForEdit = action.payload.regulationForEdit;
      state.error = null;
    },

    // getRegulationById
    regulationSelected: (state, action) => {
      state.actionsLoading = false;
      state.regulationForSelect = action.payload.regulationForSelect;
      state.error = null;
    },

    // getRegulationList
    regulationListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
    },

    // createRegulation
    regulationCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.entities.push(action.payload.regulation);
    },

    // updateRegulation
    regulationUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.map((entity) => {
        if (entity.id === action.payload.regulation.id) {
          return action.payload.regulation;
        }
        return entity;
      });
    },

    // deleteRegulation
    regulationDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(
        (el) => el.id !== action.payload.id
      );
    },

    // regulationUpdateState
    regulationStatusUpdated: (state, action) => {
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

    // getRegulationList
    materialCategoriesListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.materialCategoryList = entities;
      state.totalCount = totalCount;
    },

    // getRegulationList
    productCategoriesListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.productCategoryList = entities;
      state.totalCount = totalCount;
    },

    documentListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.documentList = entities;
      state.totalCount = totalCount;
    },
    topicListFetched: (state, action) => {
      state.actionsLoading = false;
      state.topicList = action.payload.entities;
      state.error = null;
    },

    userListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.userList = entities;
      state.totalCount = totalCount;
    },

    urlListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.urlList = entities;
      state.totalCount = totalCount;
    },
    regulationTypeFetched: (state, action) => {
      state.actionsLoading = false;
      state.regulationTypeList = action.payload.entities;
      state.error = null;
    },
    statusFetched: (state, action) => {
      state.actionsLoading = false;
      state.statusList = action.payload.entities;
      state.error = null;
    },
    languageFetched: (state, action) => {
      state.actionsLoading = false;
      state.languageList = action.payload.entities;
      state.error = null;
    },
    regulatoryFrameworkFetched: (state, action) => {
      state.actionsLoading = false;
      state.regulatoryFrameworkList = action.payload.entities;
      state.error = null;
    },

    // drop last added attachments
    milestoneDropLastAttachments: (state) => {
      state.lastAddedUrl = null;
      state.lastAddedDocument = null;
    },

    //related urls table

    //create
    regulationUrlCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.regulationForEdit.urls.push(action.payload.url);
      state.urlList.push(action.payload.url);
    },

    milestoneUrlCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.lastAddedUrl = action.payload.url;
      state.urlList.push(action.payload.url);
    },

    milestoneUrlUpdated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      const updatedUrl = action.payload.url;
      state.urlList = state.urlList.map((entity) =>
        (entity.id === updatedUrl.id)
          ? {
            ...updatedUrl,
            type: { ...updatedUrl.type },
          }
          : entity
      );
    },

    regulationUrlsLink: (state, action) => {
      const { regulation } = action.payload;
      const urlsArray = [];

      regulation.urls.forEach(urlId => {
        const urlObject = state.urlList.find(({ id }) => id === urlId);

        if (urlObject) {
          urlsArray.push(urlObject);
        }
      })

      state.error = null;
      state.actionsLoading = false;
      state.regulationForEdit.urls = urlsArray;
    },

    regulationDocumentsLink: (state, action) => {
      const { regulation } = action.payload;
      const documentsArray = [];

      regulation.documents.forEach(documentId => {
        const documentObject = state.documentList.find(({ id }) => id === documentId);

        if (documentObject) {
          documentsArray.push(documentObject);
        }
      })

      state.error = null;
      state.actionsLoading = false;
      state.regulationForEdit.documents = documentsArray;
    },

    //update
    regulationUrlUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulationForEdit.urls = state.regulationForEdit.urls.map(
        (entity) => {
          if (entity.id === action.payload.url.id) {
            return action.payload.url;
          }
          return entity;
        }
      );
    },

    //delete
    linkDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulationForEdit.urls = state.regulationForEdit.urls.filter(
        (url) => url !== action.payload.id
      );
    },

    //regulation related documents or attachments

    regulationDocumentCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.regulationForEdit.documents.push(action.payload.document);
      let data = action.payload.document;
      data.type = { id: data.type, name: action.payload.typeName };
      state.documentList.push(data);
    },
    milestoneDocumentCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.lastAddedDocument = action.payload.document;
      state.documentList.push(action.payload.document);
    },
    milestoneDocumentUpdated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      const updatedDocument = action.payload.document
      state.documentList = state.documentList.map((entity) =>
        (entity.id === updatedDocument.id)
        ? {
            ...updatedDocument,
            type: { ...updatedDocument.type },
          }
        : entity
      );
    },
    //update
    regulationDocumentUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.documentList = state.documentList.map((entity) => {
        if (entity.id === action.payload.data.id) {
          let data = action.payload.data;
          data.type = { id: data.type, name: action.payload.typeName };
          return data;
        }
        return entity;
      });
    },
    //delete
    documentsDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulationForEdit.documents = state.regulationForEdit.documents.filter(
        (doc) => doc !== action.payload.id
      );
    },

    //Impact Assessments table

    // get RegulationImpactAssessment By Id
    regulationImpactAssessmentFetched: (state, action) => {
      state.actionsLoading = false;
      state.regulationImpactAssessmentForEdit =
        action.payload.regulationImpactAssessmentForEdit;
      state.error = null;
    },

    regulationImpactAssessmentAnswersFetched: (state, action) => {
      state.actionsLoading = false;
      state.impactAssessmentAnswers = action.payload.answers;
      state.error = null;
    },

    //create
    regulationImpactAssessmentCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.regulationForEdit.impactAssessment.push(
        action.payload.impactAssessment.id
      );
      state.impactAssessmentList.push(action.payload.impactAssessment);
    },

    //update
    regulationImpactAssessmentUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulationForEdit.impactAssessment = state.regulationForEdit.impactAssessment.map(
        (entity) => {
          if (entity.id === action.payload.impactAssessment.id) {
            return action.payload.impactAssessment;
          }
          return entity;
        }
      );
    },

    //delete
    ImpactAssessmentDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulationForEdit.impactAssessment = state.regulationForEdit.impactAssessment.filter(
        (impactAssessment) => impactAssessment !== action.payload.id
      );
    },

    //updated answers
    regulationImpactAssessmentAnswersUpdated: (state, action) => {
      let { currentAns, selectedQuestionsId } = action.payload;
      state.actionsLoading = false;
      let newAns = 0;
      let data = currentAns.map((ca) => {
        let ans = state.impactAssessmentAnswers.find((x) => x.id === ca.id);
        if (!ans) newAns++;
        return { ...ans, ...ca };
      });

      state.impactAssessmentAnswers = [...data];
      state.regulationImpactAssessmentForEdit.questions[
        selectedQuestionsId
      ].answered =
        newAns === 0
          ? state.regulationImpactAssessmentForEdit.questions[
              selectedQuestionsId
            ].answered
          : state.regulationImpactAssessmentForEdit.questions[
              selectedQuestionsId
            ].answered + newAns;

      state.error = null;
    },

    // Related Milestones Slices

    relatedMilestoneCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.success = true;
      state.relatedMilestones.push(action.payload.milestone);
    },

    relatedMilestoneUpdated: (state, action) => {
      state.error = null;
      state.success = true;
      state.actionsLoading = false;
      state.relatedMilestoneForEdit = action.payload.milestone;
      state.relatedMilestones = state.relatedMilestones.map((entity) => {
        if (entity.id === action.payload.milestone.id) {
          return action.payload.milestone;
        }
        return entity;
      });
    },

    relatedMilestoneListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.relatedMilestones = entities;
      state.totalCount = totalCount;
    },

    relatedMilestoneFetched: (state, action) => {
      state.actionsLoading = false;
      state.relatedMilestoneForEdit = action.payload.relatedMilestoneForEdit;
      state.error = null;
    },

    relatedMilestoneDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.users = state.relatedMilestones.filter(
        (milestone) => milestone.id !== action.payload.id
      );
    },

    milestoneTypeListFetched: (state, action) => {
      state.actionsLoading = false;
      state.milestoneTypeList = action.payload.entities;
      state.error = null;
    },

    // filtering
    updateFilter: (state, action) => {
      state.filterOptions = {
        ...state.filterOptions,
        ...action.payload
      };
    },

    applyFilter: (state) => {
      state.isFiltered = true;
    },

    resetFilter: (state) => {
      state.filterOptions = { ...initialRegulationState.filterOptions };
      state.isFiltered = false;
    },

    updateSearchValue: (state, action) => {
      state.searchValue = action.payload;
    }
  },
});

export const { updateFilter, applyFilter, resetFilter, updateSearchValue } = regulationSlice.actions;

