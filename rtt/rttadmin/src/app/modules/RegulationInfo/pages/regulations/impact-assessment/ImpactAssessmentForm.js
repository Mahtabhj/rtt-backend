import { parseISO, toDate } from "date-fns";
import { Field, Form, Formik } from "formik";
import React, { useState } from "react";
import { Modal } from "react-bootstrap";

export function ImpactAssessmentForm({
  impactAssessment,
  actionsLoading,
  setShowImpactAssessmentAddModal,
  saveRegulationImpactAssessmentAnswers,
  regulationId,
  selectedQuestionsId,
  impactAssessmentAnswers,
  currentAnswers,
  authUser,
  userList,
}) {
  const getFullDate = (dateObj) => {
    let date =
      dateObj.getDate() < 10 ? "0" + dateObj.getDate() : dateObj.getDate();
    let month =
      dateObj.getMonth() + 1 < 10
        ? "0" + (dateObj.getMonth() + 1)
        : dateObj.getMonth() + 1;
    let year = dateObj.getFullYear();

    return date + "-" + month + "-" + year;
  };

  const [currentAns, setCurrentAns] = useState("");

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={{ ...impactAssessment.questions[selectedQuestionsId] }}
        onSubmit={(values) => {
          values.answers = currentAnswers;
          saveRegulationImpactAssessmentAnswers(
            values.answers,
            selectedQuestionsId
          );
        }}
      >
        {({ handleSubmit, errors, values }) => (
          <>
            <Modal.Body className="overlay overlay-block cursor-default">
              {actionsLoading && (
                <div className="overlay-layer bg-transparent">
                  <div className="spinner spinner-lg spinner-success" />
                </div>
              )}
              <Form className="form form-label-right">
                {values.questions.map((question, index) => {
                  const answer =
                    impactAssessmentAnswers &&
                    impactAssessmentAnswers.find(
                      (ans) =>
                        ans.question === question.id &&
                        ans.regulation === Number(regulationId)
                    );
                  const dateCreated = getFullDate(
                    toDate(parseISO(answer?.created))
                  );
                  const dateModified = getFullDate(
                    toDate(parseISO(answer?.modified))
                  );
                  const inChargePerson = userList && userList.find(
                    (user) => user.id === question.in_charge
                  ).username;
                  const answeredBy = answer?.answered_by && userList &&
                    userList.find((user) => user.id === answer?.answered_by)
                      .username;

                  return (
                    <div className="form-group row" key={index}>
                      <div className="col-lg-12">
                        <label>{question.name}</label>
                        <div className="d-flex row">
                          <div className="col-lg-6">
                            <Field
                              id={answer?.id}
                              name="answer"
                              as="textarea"
                              className="form-control"
                              placeholder="Your answer"
                              defaultValue={answer?.answer_text}
                              onChange={(e) => {
                                let ans = {};
                                ans.id = answer?.id;
                                ans.answer_text = e.target.value;
                                ans.question = question.id;
                                ans.regulation = regulationId;
                                ans.answered_by = authUser.id;
                                setCurrentAns(ans);
                              }}
                              onFocus={(e) => {
                                if (currentAns !== "") {
                                  let inserted = false;
                                  currentAnswers.find((ca, index) => {
                                    if (ca.question === currentAns.question) {
                                      currentAnswers[index] = currentAns;
                                      inserted = true;
                                    }
                                    return true;
                                  });
                                  if (!inserted)
                                    currentAnswers.push(currentAns);
                                  setCurrentAns("");
                                }
                              }}
                            />
                          </div>
                          <div className="col-lg-6">
                            <p>
                              <strong>In charge:</strong> {inChargePerson}
                            </p>
                            {answer?.answered_by && (
                              <p>
                                <strong>Answered by:</strong> {answeredBy},{" "}
                                {dateCreated}
                              </p>
                            )}
                            {answer?.answered_by && (
                              <p>
                                <strong>Last edited by:</strong> {answeredBy}{" "}
                                <strong>on</strong> {dateModified}
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </Form>
            </Modal.Body>
            <Modal.Footer>
              <button
                type="button"
                onClick={() => setShowImpactAssessmentAddModal(false)}
                className="btn btn-light btn-elevate"
              >
                Cancel
              </button>
              <> </>
              <button
                type="submit"
                onClick={() => {
                  if (currentAns !== "") {
                    let inserted = false;
                    currentAnswers.find((ca, index) => {
                      if (ca.question === currentAns.question) {
                        currentAnswers[index] = currentAns;
                        inserted = true;
                      }
                      return true;
                    });
                    if (!inserted) currentAnswers.push(currentAns);
                    setCurrentAns("");
                  }
                  handleSubmit();
                }}
                className="btn btn-primary btn-elevate"
              >
                Save
              </button>
            </Modal.Footer>
          </>
        )}
      </Formik>
    </>
  );
}
