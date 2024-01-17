import React from "react";

import { Modal } from "react-bootstrap";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-regulation/regulation/regulationActions";
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
  regulationId,
}) {
  const {
    actionsLoading,
    regulationImpactAssessmentForEdit,
    impactAssessmentAnswers,
    authUser,
    userList,
  } = useSelector(
    (state) => ({
      actionsLoading: state.regulation.actionsLoading,
      regulationImpactAssessmentForEdit:
        state.regulation.regulationImpactAssessmentForEdit,
      impactAssessmentAnswers: state.regulation.impactAssessmentAnswers,
      authUser: state.auth.user,
      userList: state.regulation.userList,
    }),
    shallowEqual
  );

  const dispatch = useDispatch();

  let currentAnswers = [];

  impactAssessmentAnswers.forEach((a) => {
    if (a.regulation === Number(regulationId)) {
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
        actions.updateRegulationImpactAssessmentAnswers({
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
          Regulation Impact Assessment Q/A
        </Modal.Title>
      </Modal.Header>

      <ImpactAssessmentForm
        setShowImpactAssessmentAddModal={setShowImpactAssessmentAddModal}
        saveRegulationImpactAssessmentAnswers={
          saveRegulationImpactAssessmentAnswers
        }
        selectedQuestionsId={selectedQuestionsId}
        regulationId={regulationId}
        impactAssessment={
          regulationImpactAssessmentForEdit || initImpactAssessment
        }
        impactAssessmentAnswers={impactAssessmentAnswers}
        currentAnswers={currentAnswers}
        authUser={authUser}
        userList={userList}
      />
    </Modal>
  );
}
