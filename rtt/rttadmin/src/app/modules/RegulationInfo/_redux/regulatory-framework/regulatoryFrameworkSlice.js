import { createSlice } from "@reduxjs/toolkit";

const initialRegulatoryFrameworkState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  regulatoryFrameworkForEdit: undefined,
  regulatoryFrameworkForSelect: undefined,
  lastError: null,
  userList: null,
  milestoneTypeList: undefined,
  success: false,
  urls: null,
  documentList: null,
  topicList: null,
  lastAddedDocument: null,
  lastAddedUrl: null,
  isFiltered: false,
  filterOptions: {
    issuing_body: null,
    status: null,
    regions: null,
    material_categories: null,
    product_categories: null,
    review_status: null
  },
  searchValue: '',
};

export const callTypes = {
  list: "list",
  action: "action",
};

export const regulatoryFrameworkSlice = createSlice({
  name: "regulatoryFramework",
  initialState: initialRegulatoryFrameworkState,
  reducers: {
    catchError: (state, action) => {
      state.error = `${action.type}: ${action.payload.error}`;
      state.success = false;
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
        state.regulatoryFrameworkForSelect =
          initialRegulatoryFrameworkState.regulatoryFrameworkForSelect;
      } else {
        state.actionsLoading = true;
        state.regulatoryFrameworkForSelect =
          initialRegulatoryFrameworkState.regulatoryFrameworkForSelect;
      }
    },

    // getRegulatoryFrameworkById
    regulatoryFrameworkFetched: (state, action) => {
      state.actionsLoading = false;
      state.regulatoryFrameworkForEdit =
        action.payload.regulatoryFrameworkForEdit;
      state.error = null;
    },

    topicListFetched: (state, action) => {
      state.actionsLoading = false;
      state.topicList = action.payload.entities;
      state.error = null;
    },

    // getRegulatoryFrameworkById
    regulatoryFrameworkSelected: (state, action) => {
      state.actionsLoading = false;
      state.regulatoryFrameworkForSelect =
        action.payload.regulatoryFrameworkForSelect;
      state.error = null;
    },

    // getRegulatoryFrameworkList
    regulatoryFrameworkListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
    },

    // createRegulatoryFramework
    regulatoryFrameworkCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.entities.push(action.payload.regulatoryFramework);
    },

    regulatoryFrameworkRelatedRegulationCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.success = true;
      state.related_regulation.push(action.payload.regulation);
    },

    regulatoryFrameworkLinkCreated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulatoryFrameworkForEdit.urls.push(action.payload.link);
    },

    // updateRegulatoryFramework
    regulatoryFrameworkUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.map((entity) => {
        if (entity.id === action.payload.regulatoryFramework.id) {
          return action.payload.regulatoryFramework;
        }
        return entity;
      });
    },

    regulatoryFrameworkRelatedRegulationUpdated: (state, action) => {
      state.error = null;
      state.success = true;
      state.actionsLoading = false;
      state.regulatoryFrameworkRelatedRegulationForEdit =
        action.payload.regulation;
      state.related_regulation = state.related_regulation.map((entity) => {
        if (entity.id === action.payload.regulation.id) {
          return action.payload.regulation;
        }
        return entity;
      });
    },

    regulatoryFrameworkLinkUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulatoryFrameworkForEdit.urls = state.regulatoryFrameworkForEdit.urls.map(
        (entity) => {
          if (entity.id === action.payload.link.id) {
            return action.payload.link;
          }
          return entity;
        }
      );
    },

    // deleteRegulatoryFramework
    regulatoryFrameworkDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(
        (el) => el.id !== action.payload.id
      );
    },

    regulatoryFrameworkRelatedRegulationListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.related_regulation = entities;
      state.totalCount = totalCount;
    },

    regulatoryFrameworkRelatedRegulationFetched: (state, action) => {
      state.actionsLoading = false;
      state.regulatoryFrameworkRelatedRegulationForEdit =
        action.payload.regulatoryFrameworkRelatedRegulationForEdit;
      state.error = null;
    },

    // regulatoryFrameworkUpdateState
    regulatoryFrameworkStatusUpdated: (state, action) => {
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
    regulatoryFrameworkRelatedRegulationDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.related_regulation = state.related_regulation.filter(
        (regulation) => regulation.id !== action.payload.id
      );
    },
    linkDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulatoryFrameworkForEdit.urls = state.regulatoryFrameworkForEdit.urls.filter(
        (link) => link.id !== action.payload.id
      );
    },

    regulatoryFrameworkUrlsLink: (state, action) => {
      const { regulatoryFramework } = action.payload;
      const urlsArray = [];

      regulatoryFramework.urls.forEach((url) => {
        const urlObject = state.urls.find((urlFromList) => urlFromList.id === url);

        if (urlObject) {
          urlsArray.push(urlObject);
        }
      })

      state.error = null;
      state.actionsLoading = false;
      state.regulatoryFrameworkForEdit.urls = urlsArray;
    },

    regulatoryFrameworkDocumentsLink: (state, action) => {
      const { regulatoryFramework } = action.payload;
      const documentsArray = [];

      regulatoryFramework.documents.forEach((document) => {
        const documentObject = state.documentList.find(({ id }) => id === document);

        if (documentObject) {
          documentsArray.push(documentObject);
        }
      })

      state.error = null;
      state.actionsLoading = false;
      state.regulatoryFrameworkForEdit.documents = documentsArray;
    },

    // Related Milestones Slices

    relatedMilestoneCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.relatedMilestones.push(action.payload.milestone);
    },

    relatedMilestoneUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.relatedMilestoneForEdit = action.payload.milestone;
      state.relatedMilestones = state.relatedMilestones.map((entity) => {
        if (entity.id === action.payload.milestone.id) {
          return action.payload.milestone;
        }
        return entity;
      });
    },

    // drop last added attachments
    milestoneDropLastAttachments: (state) => {
      state.lastAddedUrl = null;
      state.lastAddedDocument = null;
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
    languageListFetched: (state, action) => {
      state.actionsLoading = false;
      state.languageList = action.payload.entities;
      state.error = null;
    },
    statusListFetched: (state, action) => {
      state.actionsLoading = false;
      state.statusList = action.payload.entities;
      state.error = null;
    },
    issueListFetched: (state, action) => {
      state.actionsLoading = false;
      state.issueList = action.payload.entities;
      state.error = null;
    },
    regulationTypeListFetched: (state, action) => {
      state.actionsLoading = false;
      state.regulationTypeList = action.payload.entities;
      state.error = null;
    },
    productCategoryListFetched: (state, action) => {
      state.actionsLoading = false;
      state.productCategoryList = action.payload.entities;
      state.error = null;
    },
    materialCategoryListFetched: (state, action) => {
      state.actionsLoading = false;
      state.materialCategoryList = action.payload.entities;
      state.error = null;
    },

    userListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.userList = entities;
      state.totalCount = totalCount;
    },

    linkListFetched: (state, action) => {
      state.actionsLoading = false;
      state.urls = action.payload.entities;
      state.error = null;
    },
    milestoneTypeListFetched: (state, action) => {
      state.actionsLoading = false;
      state.milestoneTypeList = action.payload.entities;
      state.error = null;
    },

    urlCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.lastAddedUrl = action.payload.url;
      state.urls.push(action.payload.url);
    },

    urlUpdated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      const updatedUrl = action.payload.url;
      state.urls = state.urls.map((entity) =>
        (entity.id === updatedUrl.id)
          ? {
            ...updatedUrl,
            type: { ...updatedUrl.type },
          }
          : entity
      );
    },

    //Impact Assessments table

    // get RegulatoryFramework ImpactAssessment By id
    regulatoryFrameworkImpactAssessmentFetched: (state, action) => {
      state.actionsLoading = false;
      state.regulatoryFrameworkImpactAssessmentForEdit =
        action.payload.regulatoryFrameworkImpactAssessmentForEdit;
      state.error = null;
    },

    regulatoryFrameworkImpactAssessmentAnswersFetched: (state, action) => {
      state.actionsLoading = false;
      state.impactAssessmentAnswers = action.payload.answers;
      state.error = null;
    },

    //create
    regulatoryFrameworkImpactAssessmentCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.regulatoryFrameworkForEdit.impactAssessment.push(
        action.payload.impactAssessment.id
      );
      state.impactAssessmentList.push(action.payload.impactAssessment);
    },

    //update
    regulatoryFrameworkImpactAssessmentUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulatoryFrameworkForEdit.impactAssessment = state.regulatoryFrameworkForEdit.impactAssessment.map(
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
      state.regulatoryFrameworkForEdit.impactAssessment = state.regulatoryFrameworkForEdit.impactAssessment.filter(
        (impactAssessment) => impactAssessment !== action.payload.id
      );
    },

    //updated answers
    regulatoryFrameworkImpactAssessmentAnswersUpdated: (state, action) => {
      let { currentAns, selectedQuestionsId } = action.payload;
      state.actionsLoading = false;
      let newAns = 0;
      let data = currentAns.map((ca) => {
        let ans = state.impactAssessmentAnswers.find((x) => x.id === ca.id);
        if (!ans) newAns++;
        return { ...ans, ...ca };
      });

      state.impactAssessmentAnswers = [...data];
      state.regulatoryFrameworkImpactAssessmentForEdit.questions[
        selectedQuestionsId
      ].answered =
        newAns === 0
          ? state.regulatoryFrameworkImpactAssessmentForEdit.questions[
              selectedQuestionsId
            ].answered
          : state.regulatoryFrameworkImpactAssessmentForEdit.questions[
              selectedQuestionsId
            ].answered + newAns;

      state.error = null;
    },

    //Regulatory framework related documents or attachments

    regulatoryFrameworkDocumentCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.regulatoryFrameworkForEdit.documents.push(action.payload.document);
    },

    //update
    regulatoryFrameworkDocumentUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulatoryFrameworkForEdit.documents = state.regulatoryFrameworkForEdit.documents.map(
        (entity) => {
          if (entity.id === action.payload.document.id) {
            return action.payload.document;
          }
          return entity;
        }
      );
    },
    //delete
    documentsDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.regulatoryFrameworkForEdit.documents = state.regulatoryFrameworkForEdit.documents.filter(
        (doc) => doc !== action.payload.id
      );
    },

    documentListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.documentList = entities;
      state.totalCount = totalCount;
    },

    documentCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.lastAddedDocument = action.payload.document;
      state.documentList.push(action.payload.document);
    },

    documentUpdated: (state, action) => {
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
      state.filterOptions = { ...initialRegulatoryFrameworkState.filterOptions };
      state.isFiltered = false;
    },

    updateSearchValue: (state, action) => {
      state.searchValue = action.payload;
    }
  },
});

export const { updateFilter, applyFilter, resetFilter, updateSearchValue } = regulatoryFrameworkSlice.actions;

