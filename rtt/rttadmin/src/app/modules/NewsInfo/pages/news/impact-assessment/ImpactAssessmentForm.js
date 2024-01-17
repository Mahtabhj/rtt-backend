import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Modal } from "react-bootstrap";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import Select from "react-select";
import Slider from "@material-ui/core/Slider";
import RichTextEditor from "react-rte";

// Validation schema
const ImpactAssessmentEditSchema = Yup.object().shape({
  relevancy: Yup.string().required("Relevancy is required"),
  comment: Yup.object().required("Comment is required"),
  organisation: Yup.string()
    .ensure()
    .required("Organisation is required"),
});

export function ImpactAssessmentForm({
  newsId,
  impactAssessment,
  actionsLoading,
  setShowImpactAssessmentAddModal,
  saveNewsRelatedImpactAssessment,
}) {
  const { organizationList } = useSelector(
    (state) => ({
      organizationList: state.news.organizationList,
    })
  );

  const [organizationOptions, setOrganizationOptions] = useState([]);
  const [organizationSelected, setOrganizationSelected] = useState(null);
  const [value, setValue] = useState(0);

  useEffect(() => {
    const organizationOption = organizationList && organizationList.map((option) => ({ value: option.id, label: option.name }));

    if (impactAssessment.id) {
      setOrganizationSelected(
        organizationOption.find(
          (org) => org.value === impactAssessment.organization
        )
      );
    } else {
      setOrganizationSelected(organizationOption[0]);
    }

    setOrganizationOptions(organizationOption);
  }, [impactAssessment, organizationList]);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  function valuetext(value) {
    return `${value}°C`;
  }

  return (
    <>
      <Formik
        enableReinitialize
        initialValues={{
          ...impactAssessment,
          relevancy: value || impactAssessment.relevancy || 0,
          organisation: organizationSelected ? organizationSelected?.value : impactAssessment.organization,
          news: newsId,
        }}
        validationSchema={ImpactAssessmentEditSchema}
        onSubmit={(values) => {
          const finalValues = {
            id: values.id || undefined,
            news: newsId,
            organization: values.organisation,
            relevancy: values.relevancy,
            comment: values.comment.toString("html"),
          };

          saveNewsRelatedImpactAssessment(finalValues);
        }}
      >
        {({ handleSubmit, errors, values, setFieldValue }) => {
          return (
            <>
              <Modal.Body className="overlay overlay-block cursor-default">
                {actionsLoading && (
                  <div className="overlay-layer bg-transparent">
                    <div className="spinner spinner-lg spinner-success" />
                  </div>
                )}
                <Form className="form form-label-right">
                  <div className="form-group row">
                    {/* First Name */}

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
                      <Slider
                        disabled={false}
                        name="relevancy"
                        value={values.relevancy}
                        marks
                        step={1}
                        min={0}
                        max={5}
                        getAriaValueText={valuetext}
                        onChange={handleChange}
                        aria-labelledby="discrete-slider"
                        valueLabelDisplay="auto"
                        style={{ marginTop: '30px' }}
                      />

                      {errors.relevancy && <p className="text-danger"> {errors.relevancy} </p>}
                      {/*<label>News</label>*/}
                      {/*<Field*/}
                      {/*  name="news"*/}
                      {/*  component={() => (*/}
                      {/*    <Select*/}
                      {/*      isMulti={false}*/}
                      {/*      options={newsOptions}*/}
                      {/*      value={newsSelected}*/}
                      {/*      onChange={(e) => setNewsSelected(e)}*/}
                      {/*    />*/}
                      {/*  )}*/}
                      {/*/>*/}
                    </div>
                  </div>

                  <div className="form-group row">
                    <div className="col-lg-12">
                      <label>Comment</label>

                      <RichTextEditor
                        value={values.comment}
                        onChange={(value) => setFieldValue('comment', value)}
                      />

                      {errors.comment ? (
                        <p className="text-danger"> {errors.comment} </p>
                      ) : null}
                    </div>
                  </div>
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
                  onClick={() => handleSubmit()}
                  className="btn btn-primary btn-elevate"
                >
                  Save
                </button>
              </Modal.Footer>
            </>
          )
        }}
      </Formik>
    </>
  );
}
