import React from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { Input } from "@metronic-partials/controls";

// Validation schema
const IndustryEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(150, "Maximum 150 symbols")
    .required("Name is required"),
  description: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(250, "Maximum 250 symbols")
    .required("Description required"),
});

export function IndustryEditForm({ industry, btnRef, saveIndustry }) {
  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={industry}
        validationSchema={IndustryEditSchema}
        onSubmit={(values) => {
          saveIndustry(values);
        }}
      >
        {({ handleSubmit }) => (
          <>
            <Form className="form form-label-right">
              <div className="form-group row">
                {/* Name */}
                <div className="col-lg-6">
                  <Field
                    name="name"
                    component={Input}
                    placeholder="Name"
                    label="Name *"
                    withFeedbackLabel={false}
                  />
                </div>

                {/* Description */}
                <div className="col-lg-6">
                  <Field
                    name="description"
                    component={Input}
                    placeholder="Description"
                    label="Description *"
                    withFeedbackLabel={false}
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
