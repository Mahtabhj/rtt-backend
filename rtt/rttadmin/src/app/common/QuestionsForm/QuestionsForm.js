import React, { useEffect, useState } from "react";
import { Field } from "formik";
import PropTypes from "prop-types";

const propTypes = {
  questions: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    organization: PropTypes.number.isRequired,
  })).isRequired,
  setAnswersCallback: PropTypes.func.isRequired,
};

export function QuestionsForm({ questions, setAnswersCallback }) {
  const [answers, setAnswers] = useState(null);

  useEffect(() => {
    if (!answers && questions?.length) {
      const createdAnswers = questions.map(({ id }) => ({ question_id: id, answer_text: '' }));
      setAnswers(createdAnswers);
      setAnswersCallback(createdAnswers);
    }
  }, [questions, setAnswersCallback, answers]);

  const handleOnChange = questionId => ({ target: { value } }) => {
    const updatedAnswers = answers.map(answer =>
      answer.question_id === questionId ? ({ question_id: questionId, answer_text: value }) : answer
    );
    setAnswers(updatedAnswers);
    setAnswersCallback(updatedAnswers);
  }

  return (
    <>
      {questions.map(question => (
        <div className="form-group row" key={question.id}>
          <div className="col-lg-12">
            <label><strong>{question.name}</strong> ({question.description})</label>
            <Field
              id={question.id}
              name="answer"
              as="textarea"
              className="form-control"
              placeholder="Your answer"
              onChange={handleOnChange(question.id)}
            />
          </div>
        </div>
      ))}
    </>
  );
}

QuestionsForm.propTypes = propTypes;
