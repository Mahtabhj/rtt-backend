import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Modal } from "react-bootstrap";
import RichTextEditor from "react-rte";
import dayjs from "dayjs";
import PropTypes from "prop-types";

import * as regulationActions from "@redux-regulation/regulation/regulationActions";
import * as regulatoryFrameworkActions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";

import { ModalProgressBar } from "@metronic-partials/controls";

import { MilestoneForm } from "@common/Milestone/MilestoneForm";

const actions = {
  regulation: regulationActions,
  regulatoryFramework: regulatoryFrameworkActions,
};

const initMilestone = {
  id: undefined,
  name: "",
  from_date: dayjs().format("MM/DD/YYYY"),
  to_date: dayjs().format("MM/DD/YYYY"),
  description: RichTextEditor.createEmptyValue(),
  regulation: "",
  documents: [],
  urls: [],
  type: "",
};


const propTypes = {
  type: PropTypes.oneOf(['regulation', 'regulatoryFramework']).isRequired,
  isModalShown: PropTypes.bool.isRequired,
  closeModalCallback: PropTypes.func.isRequired,
  selectedMilestoneId: PropTypes.number,
  regulationId: PropTypes.number.isRequired,
}

export const MilestoneAddEditModal = ({
  type,
  isModalShown,
  closeModalCallback,
  selectedMilestoneId,
  regulationId,
}) => {
  const dispatch = useDispatch();

  const [initialMilestone, setInitialMilestone] = useState(initMilestone);

  const {
    actionsLoading,
    relatedMilestoneForEdit,
    milestoneTypeList = [],
    documents = [],
    urls = [],
  } = useSelector(
    (state) => ({
      actionsLoading: state[type].actionsLoading,
      relatedMilestoneForEdit: state[type].relatedMilestoneForEdit,
      milestoneTypeList: state[type].milestoneTypeList,
      documents: state[type].documentList,
      urls: state[type][type === 'regulation' ? 'urlList' : 'urls'],
    })
  );

  useEffect(() => {
    if (selectedMilestoneId) {
      if (relatedMilestoneForEdit) {
        let newInit = {
          ...relatedMilestoneForEdit,
          from_date: relatedMilestoneForEdit.from_date
            ? dayjs(relatedMilestoneForEdit.from_date).format("MM/DD/YYYY")
            : null,
          to_date: relatedMilestoneForEdit.to_date
            ? dayjs(relatedMilestoneForEdit.to_date).format("MM/DD/YYYY")
            : null,
          documents: documents.filter(({ id }) => relatedMilestoneForEdit.documents.includes(id)),
          urls: urls.filter(({ id }) => relatedMilestoneForEdit.urls.includes(id)),
          description: RichTextEditor.createValueFromString(relatedMilestoneForEdit.description, "html"),
        };

        setInitialMilestone(newInit);
      }
    } else {
      setInitialMilestone(initMilestone);
    }
  }, [
    selectedMilestoneId,
    relatedMilestoneForEdit,
    documents,
    urls,
  ]);

  useEffect(() => {
    dispatch(actions[type].fetchMilestoneTypeList());
  }, [type, dispatch]);

  useEffect(() => {
    dispatch(actions[type].fetchRelatedMilestone(selectedMilestoneId));
  }, [type, dispatch, selectedMilestoneId]);

  const saveRelatedMilestone = (values) => {
    const isDescriptionEmpty = values.description.toString("markdown").trim() === '\u200b';

    const payload = {
      ...values,
      description: isDescriptionEmpty ? '' : values.description.toString("html"),
    };

    if (!selectedMilestoneId) {
      dispatch(
        actions[type].createRelatedMilestone({
          ...payload,
          [type === 'regulation' ? 'regulation' : 'regulatory_framework']: regulationId,
        })
      ).then(() => {
        closeModalCallback();
        dispatch(actions[type].fetchRelatedMilestoneList(regulationId));
      });
    } else {
      dispatch(actions[type].updateRelatedMilestone(payload)).then(() => {
        closeModalCallback();
        dispatch(actions[type].fetchRelatedMilestoneList(regulationId));
      })
    }
  };

  return isModalShown && (
    <Modal
      size="lg"
      show={isModalShown}
      onHide={() => closeModalCallback()}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}

      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {selectedMilestoneId ? "Edit" : "Add"} Milestone
        </Modal.Title>
      </Modal.Header>

      <MilestoneForm
        type={type}
        setShowMilestoneAddModal={closeModalCallback}
        saveRelatedMilestone={saveRelatedMilestone}
        milestone={initialMilestone}
        milestoneTypeList={milestoneTypeList}
        documents={documents}
        urls={urls}
        actionsLoading={actionsLoading}
      />
    </Modal>
  );
}

MilestoneAddEditModal.propTypes = propTypes;
