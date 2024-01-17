import React, { useState, useEffect } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { Input, Select as MetSelect } from "@metronic-partials/controls";
import Select from "react-select";

import { getIndustryList } from "@redux/commonApiService";

// Validation schema
const MaterialCategoryEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(150, "Maximum 150 symbols")
    .required("Name is required"),
  description: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(250, "Maximum 250 symbols")
    .required("Description required"),
  industry: Yup.string()
    .ensure()
    .required("Industry is required"),
});

export function MaterialCategoryEditForm({
  materialCategory,
  btnRef,
  saveMaterialCategory,
}) {
  const [industryOptions, setIndustryOptions] = useState([]);
  const [file, setFile] = useState(null);

  useEffect(() => {
    // Get Industry dropdown options
    getIndustryList()
      .then((response) => {
        const industryOptions = response.data.results.map((option) => {
          return { value: option.id, label: option.name };
        });
        setIndustryOptions(industryOptions);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={materialCategory}
        validationSchema={MaterialCategoryEditSchema}
        onSubmit={(values) => {
          saveMaterialCategory(values);
        }}
      >
        {({ handleSubmit, setFieldValue }) => (
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

              <div className="form-group row">
                {/* Industry */}
                <div className="col-lg-6">
                  <label>Industry *</label>
                  <Field
                    name="industry"
                    component={({ field, form }) => (
                      <Select
                        isMulti={false}
                        options={industryOptions}
                        value={
                          industryOptions
                            ? industryOptions.find(
                                (opt) => opt.value === field.value
                              )
                            : ""
                        }
                        onChange={(option) =>
                          form.setFieldValue(field.name, option.value)
                        }
                        onBlur={field.onBlur}
                      />
                    )}
                  />
                  <ErrorMessage name="industry">
                    {(msg) => <div style={{ color: "red" }}>{msg}</div>}
                  </ErrorMessage>
                </div>

                {/* Online */}
                <div className="col-lg-6">
                  <MetSelect
                    name="online"
                    label="Online"
                    withFeedbackLabel={false}
                  >
                    <option key="online" value={true}>
                      Online
                    </option>
                    <option key="offline" value={false}>
                      Offline
                    </option>
                  </MetSelect>
                </div>
              </div>
              <div className="form-group row">
                <div className="col-lg-6">
                  <label>Select File</label>
                  <input
                    id="cover_image"
                    name="image"
                    type="file"
                    onChange={(event) => {
                      setFieldValue("image", event.currentTarget.files[0]);
                      setFile(
                        URL.createObjectURL(event.currentTarget.files[0])
                      );
                    }}
                    className="form-control"
                  />
                </div>
                <div className="col-lg-6">
                  {file ? (
                    <img
                      className="ml-auto"
                      height="150"
                      width="300"
                      src={file}
                      alt="cover"
                    ></img>
                  ) : materialCategory.image !== "" ? (
                    <img
                      className="ml-auto"
                      height="150"
                      width="300"
                      src={materialCategory.image}
                      alt="cover"
                    ></img>
                  ) : null}
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
