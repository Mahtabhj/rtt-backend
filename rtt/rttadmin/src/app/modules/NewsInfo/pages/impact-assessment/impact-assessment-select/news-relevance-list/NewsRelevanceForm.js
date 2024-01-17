import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Select from "react-select";
import { Modal } from "react-bootstrap";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

import {
  addImpactAssessmentAnswers,
  fetchImpactAssessmentQuestions
} from "@redux-news/impact-assessment/impactAssessmentActions";

import { RatingStars, QuestionsForm } from "@common";

// Validation schema
const NewsRelevanceEditSchema = Yup.object().shape({
  relevancy: Yup.number().test('IS NOT 0', 'Relevancy is required', value => value),
  answers: Yup.object(),
  organisation: Yup.string().ensure().required("Organisation is required"),
});

export function NewsRelevanceForm({
  newsId,
  newsRelevance,
  actionsLoading,
  setShowNewsRelevanceAddModal,
  saveNewsRelatedNewsRelevance,
}) {
  const dispatch = useDispatch();
  const { organization, questions } = useSelector(
    (state) => ({
      organization: state.newsImpactAssessment.impactAssessmentForSelect.organization,
      questions: state.newsImpactAssessment.questions,
    })
  );

  const [answers, setAnswers] = useState([]);
  const [organizationOptions, setOrganizationOptions] = useState([]);
  const [organizationSelected, setOrganizationSelected] = useState(null);

  useEffect(() => {
    if (organization) {
      const organizationOption = { value: organization.id, label: organization.name };

      setOrganizationSelected(organizationOption);

      setOrganizationOptions([organizationOption]);

      dispatch(fetchImpactAssessmentQuestions(organization.id));
    }
  }, [dispatch, organization]);

  const handleOnSubmit = (values) => {
    const finalValues = {
      id: values.id || undefined,
      news: newsId,
      organization: values.organisation,
      relevancy: values.relevancy,
    };

    dispatch(addImpactAssessmentAnswers(newsId, { assessments: answers })).then(() => {
      saveNewsRelatedNewsRelevance(finalValues);
    });
  };

  return (
    <Formik
      enableReinitialize
      initialValues={{
        ...newsRelevance,
        relevancy: newsRelevance.relevancy,
        organisation: organizationSelected ? organizationSelected?.value : newsRelevance.organization,
        news: newsId,
      }}
      validationSchema={NewsRelevanceEditSchema}
      onSubmit={handleOnSubmit}
    >
      {({ handleSubmit, errors, values, setFieldValue }) => (
        <>
          <Modal.Body className="overlay overlay-block cursor-default">
            {actionsLoading && (
              <div className="overlay-layer bg-transparent">
                <div className="spinner spinner-lg spinner-success" />
              </div>
            )}
            <Form className="form form-label-right">
              <div className="form-group row">
                <div className="col-lg-6">
                  <label>Organization</label>
                  <Field
                    name="organisation"
                    component={({ field, form }) => (
                      <Select
                        isMulti={false}
                        options={organizationOptions}
                        value={organizationSelected}
                        onChange={(e) => setOrganizationSelected(e)}
                      />
                    )}
                  />
                  <ErrorMessage name="organisation">
                    {(msg) => <div style={{ color: "#e7576c" }}>{msg}</div>}
                  </ErrorMessage>
                </div>

                <div className="col-lg-6">
                  <label>Impact rating</label>
                  <div style={{ padding: '9px 0' }}>
                    <RatingStars
                      rating={values.relevancy}
                      setRating={relevancy => setFieldValue('relevancy', +relevancy)}
                    />
                  </div>

                  {!!errors.relevancy && <p className="text-danger">{errors.relevancy}</p>}
                </div>
              </div>

              <QuestionsForm
                questions={questions}
                setAnswersCallback={setAnswers}
              />
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <button
              type="button"
              onClick={() => setShowNewsRelevanceAddModal(false)}
              className="btn btn-light btn-elevate"
            >
              Cancel
            </button>
            <button
              type="submit"
              onClick={() => handleSubmit()}
              className="btn btn-primary btn-elevate"
            >
              Save
            </button>
          </Modal.Footer>
        </>
      )}
    </Formik>
  );
}
