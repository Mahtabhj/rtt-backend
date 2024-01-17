import React, { useEffect, useState } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "../../../../../../_metronic/_partials/controls";
import * as actions from "../../../_redux/news/newsActions";
import { DocumentsForm } from "./DocumentsForm";
import RichTextEditor from 'react-rte';

const initDocumentObject = {
  id: undefined,
  title: "",
  description: RichTextEditor.createEmptyValue(),
  attachment: "",
  type: "",
};

export function DocumentsAddEditModal({
  showDocumentsAddModal,
  setShowDocumentsAddModal,
  selectedDocumentsId,
  newsId,
}) {
  const dispatch = useDispatch();

  const [initDocument, setInitDocument] = useState(initDocumentObject);
  const [isDocumentSaving, setDocumentSaving] = useState(false);

  const {
    actionsLoading,
    newsRelatedDocumentForEdit,
    documentTypeList,
  } = useSelector(
    (state) => ({
      actionsLoading: state.news.actionsLoading,
      // newsRelatedDocumentForEdit: state.news.newsRelatedDocumentForEdit,
      newsRelatedDocumentForEdit: state.news.documentList.find(
        (document) => document.id === selectedDocumentsId
      ),
      documentTypeList: state.news.documentTypeList,
    }),
    shallowEqual
  );

  useEffect(() => {
    dispatch(actions.fetchDocumentTypeList());
  }, [dispatch]);

  useEffect(() => {
    if (newsRelatedDocumentForEdit && newsRelatedDocumentForEdit.id) {
      let newInit = {
        ...newsRelatedDocumentForEdit,
        description: RichTextEditor.createValueFromString(newsRelatedDocumentForEdit.description, "html"),
      };
      setInitDocument(newInit);
    } else if (documentTypeList) {
      let newInit = {
        ...initDocument,
        type: documentTypeList.length > 0 ? documentTypeList[0].id : null,
      };
      setInitDocument(newInit);
    }

    if (!selectedDocumentsId) {
      setInitDocument({
        ...initDocumentObject,
        type: documentTypeList?.length > 0 ? documentTypeList?.[0]?.id : null,
      })
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [newsRelatedDocumentForEdit, documentTypeList, selectedDocumentsId]);

  const saveNewsRelatedDocuments = (values) => {
    setDocumentSaving(true);
    const isDescriptionEmpty = values.description.toString("markdown").trim() === '\u200b';

    const payload = {
      ...values,
      description: isDescriptionEmpty ? '' : values.description.toString("html"),
    };

    if (!selectedDocumentsId) {
      dispatch(
        actions.createNewsRelatedDocument({
          document: payload,
          newsId,
        })
      ).then(() => {
        setShowDocumentsAddModal(false);
        setDocumentSaving(false);
      });
    } else {
      dispatch(actions.updateNewsRelatedDocument(payload)).then(() => {
        setShowDocumentsAddModal(false);
        setDocumentSaving(false);
      });
    }
  };

  return (
    <Modal
      size="lg"
      show={showDocumentsAddModal}
      onHide={() => setShowDocumentsAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedDocumentsId ? "Edit" : "Add"} News Attachment
        </Modal.Title>
      </Modal.Header>

      <DocumentsForm
        setShowDocumentsAddModal={setShowDocumentsAddModal}
        saveNewsRelatedDocuments={saveNewsRelatedDocuments}
        isSaving={isDocumentSaving}
        documents={initDocument}
        documentTypeList={documentTypeList || []}
      />
    </Modal>
  );
}
