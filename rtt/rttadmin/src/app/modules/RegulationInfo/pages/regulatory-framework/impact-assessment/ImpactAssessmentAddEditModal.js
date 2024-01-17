import React from "react";

import { Modal } from "react-bootstrap";
import { ModalProgressBar } from "../../../../../../_metronic/_partials/controls";
import * as actions from "../../../_redux/regulatory-framework/regulatoryFrameworkActions";
import { shallowEqual, useDispatch, useSelector } from "react-redux";

import { ImpactAssessmentForm } from "./ImpactAssessmentForm";

const initImpactAssessment = {
  id: undefined,
  regions: "",
  regulation_name: "",
  issuing_body: "",
  questions: [],
  answers: [],
};

export function ImpactAssessmentAddEditModal({
  showImpactAssessmentAddModal,
  setShowImpactAssessmentAddModal,
  selectedQuestionsId,
  regulatoryFrameworkId,
}) {
  const {
    actionsLoading,
    regulatoryFrameworkImpactAssessmentForEdit,
    impactAssessmentAnswers,
    relatedRegulation,
    authUser,
    userList,
  } = useSelector(
    (state) => ({
      actionsLoading: state.regulatoryFramework.actionsLoading,
      regulatoryFrameworkImpactAssessmentForEdit: state.regulatoryFramework.regulatoryFrameworkImpactAssessmentForEdit,
      impactAssessmentAnswers: state.regulatoryFramework.impactAssessmentAnswers,
      relatedRegulation: state.regulatoryFramework.related_regulation,
      authUser: state.auth.user,
      userList: state.regulatoryFramework.userList,
    }),
    shallowEqual
  );

  const dispatch = useDispatch();

  let currentAnswers = [];

  impactAssessmentAnswers.forEach((a) => {
    if (relatedRegulation.filter((r) => r.id === a.regulation).length > 0) {
      let ans = {
        id: a.id,
        question: a.question,
        regulation: a.regulation,
        answered_by: a.answered_by,
        answer_text: a.answer_text,
      };

      currentAnswers.push(ans);
    }
  });

  const saveRegulatoryFrameworkImpactAssessmentAnswers = (
    values,
    selectedQuestionsId
  ) => {

    if (values) {
      dispatch(
        actions.updateRegulatoryFrameworkImpactAssessmentAnswers({
          answers: values,
          selectedQuestionsId,
        })
      );
      setShowImpactAssessmentAddModal(false);
    }
  };

  return (
    <Modal
      size="lg"
      show={showImpactAssessmentAddModal}
      onHide={() => setShowImpactAssessmentAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          RegulatoryFramework Impact Assessment Q/A
        </Modal.Title>
      </Modal.Header>

      <ImpactAssessmentForm
        setShowImpactAssessmentAddModal={setShowImpactAssessmentAddModal}
        saveRegulatoryFrameworkImpactAssessmentAnswers={saveRegulatoryFrameworkImpactAssessmentAnswers}
        selectedQuestionsId={selectedQuestionsId}
        regulatoryFrameworkId={regulatoryFrameworkId}
        impactAssessment={regulatoryFrameworkImpactAssessmentForEdit || initImpactAssessment}
        impactAssessmentAnswers={impactAssessmentAnswers}
        relatedRegulation={relatedRegulation}
        currentAnswers={currentAnswers}
        authUser={authUser}
        userList={userList}
      />
    </Modal>
  );
}
