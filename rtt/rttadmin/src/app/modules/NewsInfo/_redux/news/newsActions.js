import * as newsApiService from "./newsApiService";
import { newsSlice, callTypes } from "./newsSlice";
import { toast } from "react-toastify";

const { actions } = newsSlice;

export const fetchNewsList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getNewsList(queryParams)
    .then((response) => {
      const { count: totalCount, results: entities, review_count: reviewCount } = response.data;

      dispatch(actions.newsListFetched({ entities, totalCount, reviewCount }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchNewsRelevanceList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getNewsRelevanceList(queryParams)
    .then((response) => {
      const entities = response.data;
      dispatch(actions.newsRelevanceListFetched({ entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchSourceList = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getSourceList()
    .then((response) => {
      const entities = response.data.results;
      dispatch(actions.sourceListFetched({ entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchCategoryList = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getCategoryList()
    .then((response) => {
      const entities = response.data.results;
      dispatch(actions.categoryListFetched({ entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchRegulationList = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getRegulationList()
    .then((response) => {
      const entities = response.data.results;
      dispatch(actions.regulationListFetched({ entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchProductCategoryList = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getProductCategoryList()
    .then((response) => {
      const entities = response.data.results;
      dispatch(actions.productCategoryListFetched({ entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchMaterialCategoryList = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getMaterialCategoryList()
    .then((response) => {
      const entities = response.data.results;
      dispatch(actions.materialCategoryListFetched({ entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchOrganizationList = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getOrganizationList()
    .then((response) => {
      const entities = response.data.results;
      dispatch(actions.organizationListFetched({ entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchRegulationFrameworkList = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getRegulatoryFrameworkList()
    .then((response) => {
      const entities = response.data.results;
      dispatch(actions.regulationFrameworkFetched({ entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchDocumentList = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getDocumentList()
    .then((response) => {
      const entities = response.data.results;
      dispatch(actions.documentsFetched({ entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchNews = (id) => (dispatch) => {
  if (!id) {
    return dispatch(actions.newsFetched({ newsForEdit: undefined }));
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .getNewsById(id)
    .then((response) => {
      const news = response.data;
      dispatch(actions.newsFetched({ newsForEdit: news }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const selectNews = (id) => (dispatch) => {
  if (!id) {
    return dispatch(actions.newsSelected({ newsForSelect: undefined }));
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .getNewsById(id)
    .then((response) => {
      const news = response.data;
      dispatch(actions.newsSelected({ newsForSelect: news }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const selectNewsPatch = (id, news) => (dispatch) => {
  if (!id) {
    return dispatch(actions.newsSelected({ newsForSelect: undefined }));
  }

  dispatch(actions.newsPatching({}));
  return newsApiService
    .updateNewsPatch(id, news)
    .then(() => {
      dispatch(actions.newsPatched({}));
    })
    .catch((error) => {
      error.clientMessage = "Can't find news";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteNews = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .deleteNews(id)
    .then(() => {
      dispatch(actions.newsDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete news";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const dischargeNews = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .dischargeNews(id)
    .then((response) => {
      dispatch(actions.newsDischarged({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't discharge news";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createNews = (newsForCreation) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .createNews(newsForCreation)
    .then((response) => {
      const news = response.data;
      dispatch(actions.newsCreated({ news }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create news";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateNews = (news) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .updateNews(news)
    .then(() => {
      dispatch(actions.newsUpdated({ news }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update news";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateNewsStatus = (ids, status) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .updateStatusForNews(ids, status)
    .then(() => {
      dispatch(actions.newsStatusUpdated({ ids, status }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update news status";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateNewsReview = (id, dataToSend) => dispatch => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .updateNewsPatch(id, dataToSend)
    .then(() => {
      dispatch(actions.newsReviewUpdated({ id, dataToSend }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update news review";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const clearNewsForSelect = () => (dispatch) => {
  return dispatch(actions.newsSelected({ newsForSelect: undefined }));
};

export const clearNewsForEdit = () => (dispatch) => {
  return dispatch(actions.newsFetched({ newsForEdit: undefined }));
};

//Related attachments or documents table

export const fetchDocumentTypeList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getDocumentTypeList(queryParams)
    .then((response) => {
      const totalCount = response.count;
      const entities = response.data.results;
      dispatch(
        actions.documentTypeListFetched({
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

//Create
export const createNewsRelatedDocument = ({ document, newsId }) => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .createNewsRelatedDocument(document)
    .then(({ data: newDocument }) => {
      return newsApiService.getNewsById(newsId).then(({ data: { documents: existingDocuments } }) => {
        const documentsIds = [newDocument.id, ...existingDocuments.map(({ id }) => id)];

        return newsApiService
          .updateNewsDocuments({ newsId, documents: documentsIds })
          .then((res) => {
            dispatch(actions.newsDocumentCreated({ document: newDocument }));
          });
      });
    })
    .catch((error) => {
      error.clientMessage = "Can't create attachment";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Update
export const updateNewsRelatedDocument = (document) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .updateNewsRelatedDocument(document)
    .then(() => {
      dispatch(actions.newsDocumentUpdated({ document }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update related document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//Delete
export const deleteDocuments = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .deleteDocuments(id)
    .then((response) => {
      dispatch(actions.documentsDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete url";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//related impact assessment table

//Create
export const createNewsRelevance = (relevance) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .saveNewsRelevance(relevance)

    .then((response) => {
      dispatch(actions.newsRelevanceCreated({ relevance: response.data }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create relevance";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

//update
export const updateNewsRelevance = (relevance) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .updateNewsRelevance(relevance)
    .then(() => {
      dispatch(actions.newsRelevanceUpdated({ relevance }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update news";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteNewsRelevance = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .deleteNewsRelevance(id)
    .then(() => {
      dispatch(actions.newsRelevanceDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete news relevance";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchRegionList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return newsApiService
    .getRegionList(queryParams)
    .then((response) => {
      const regionList = response.data.results;
      dispatch(actions.regionListFetched({ regionList }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find region";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const saveNewsFromDate = (fromDate) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return newsApiService
    .saveNewsFromDate(fromDate)
    .then((response) => {
      const { status, data } = response;
      if (status === 200) {
        dispatch(actions.newsFromDateSaved(null));

        data.message && toast.success(data.message, { position: toast.POSITION.TOP_CENTER });
      }
      return response;
    })
    .catch((error) => {
      error.clientMessage = "Can't save news from date";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};
