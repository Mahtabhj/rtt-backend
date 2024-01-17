import React, { useState, useEffect } from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { Input, Select } from "@metronic-partials/controls";

// Validation schema
const ImpactAssessmentEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(150, "Maximum 150 symbols")
    .required("Name is required"),
});

export function ImpactAssessmentEditForm({
  impactAssessment,
  btnRef,
  saveImpactAssessment,
}) {
  const [regionOptions, setRegionBodyOptions] = useState([]);

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={impactAssessment}
        validationSchema={ImpactAssessmentEditSchema}
        onSubmit={(values) => {
          saveImpactAssessment(values);
        }}
      >
        {({ handleSubmit }) => (
          <>
            <Form className="form form-label-right">
              <div className="form-group mb-2 row">
                <div className="col-lg-6">
                  <Field
                    name="name"
                    component={Input}
                    withFeedbackLabel={false}
                    placeholder="Name"
                    label="Issuing Body Name"
                  />
                </div>
                <div className=" col-lg-6 mb-2 form-group">
                  <label>Region</label>
                  <Select
                    name="region"
                    defaultValue={impactAssessment.region}
                    withFeedbackLabel={false}
                  >
                    {regionOptions.map(function(region) {
                      return (
                        <option key={region.value} value={region.value}>
                          {region.label}
                        </option>
                      );
                    })}
                  </Select>
                </div>
              </div>
              <div className="form-group mb-2 row">
                <div className="col-lg-12">
                  <label>Description</label>
                  <Field
                    name="description"
                    as="textarea"
                    className="form-control"
                    placeholder="Description"
                  />
                </div>
              </div>
              <button
                type="submit"
                style={{ display: "none" }}
                ref={btnRef}
                onSubmit={() => handleSubmit()}
              ></button>
            </Form>
          </>
        )}
      </Formik>
    </>
  );
}
