import React from "react";

import { Modal } from "react-bootstrap";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/impact-assessment/impactAssessmentActions";
import { shallowEqual, useDispatch, useSelector } from "react-redux";

import { ImpactAssessmentForm } from "./ImpactAssessmentForm";

export function ImpactAssessmentAddEditModal({
  showImpactAssessmentAddModal,
  setShowImpactAssessmentAddModal,
  singleImpactAssessment,
  selectedQuestionsId,
  impactAssessmentId,
  regulationId,
}) {
  const {
    actionsLoading,
    impactAssessmentAnswers,
    authUser,
    userList,
  } = useSelector(
    (state) => ({
      actionsLoading: state.impactAssessment.actionsLoading,
      impactAssessmentAnswers: state.impactAssessment.impactAssessmentAnswers,
      authUser: state.auth.user,
      userList: state.impactAssessment.userList,
    }),
    shallowEqual
  );

  const dispatch = useDispatch();

  let currentAnswers = [];

  impactAssessmentAnswers &&
    impactAssessmentAnswers.forEach((a) => {
      if (a.regulation === regulationId) {
        let ans = {
          id: a.id,
          question: a.question,
          regulation: regulationId,
          answered_by: a.answered_by,
          answer_text: a.answer_text,
        };

        currentAnswers.push(ans);
      }
    });

  const saveRegulationImpactAssessmentAnswers = (
    values,
    selectedQuestionsId
  ) => {
    if (values) {
      dispatch(
        actions.updateImpactAssessmentAnswers({
          answers: values,
          selectedQuestionsId,
          impactAssessmentId,
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
          Impact Assessment Q/A
        </Modal.Title>
      </Modal.Header>

      <ImpactAssessmentForm
        setShowImpactAssessmentAddModal={setShowImpactAssessmentAddModal}
        saveRegulationImpactAssessmentAnswers={
          saveRegulationImpactAssessmentAnswers
        }
        selectedQuestionsId={selectedQuestionsId}
        impactAssessmentId={impactAssessmentId}
        impactAssessment={singleImpactAssessment}
        impactAssessmentAnswers={impactAssessmentAnswers}
        currentAnswers={currentAnswers}
        authUser={authUser}
        userList={userList}
        regulationId={regulationId}
      />
    </Modal>
  );
}
