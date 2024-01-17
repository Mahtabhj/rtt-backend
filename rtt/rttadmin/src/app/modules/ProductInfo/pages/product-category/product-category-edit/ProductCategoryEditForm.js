import React, { useState, useEffect } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { Input, Select as MetSelect } from "@metronic-partials/controls";
import ReactSelect from "react-select";
import * as productCategoryApiService from "@redux-product/product-category/productCategoryApiService";

// Validation schema
const ProductCategoryEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(150, "Maximum 50 symbols")
    .required("Name is required"),
  description: Yup.string()
    .min(2, "Minimum 2 symbols")
    .max(250, "Maximum 250 symbols")
    .required("Description required"),
  industry: Yup.string()
    .ensure()
    .required("Industry is required"),
});

export function ProductCategoryEditForm({
  productCategory,
  btnRef,
  saveProductCategory,
  industryList,
}) {
  const [parentOptions, setParentOptions] = useState([]);
  const [file, setFile] = useState(null);
  useEffect(() => {
    // Get Parent select options
    productCategoryApiService
      .getAllProductCategory()
      .then((response) => {
        const parentOptions = response.data.results.map((option) => {
          return { value: option.id, label: option.name };
        });
        parentOptions.unshift({ value: "", label: "" });
        setParentOptions(parentOptions);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={productCategory}
        validationSchema={ProductCategoryEditSchema}
        onSubmit={(values) => {
          values.industry = values.industry.map((a) => a.id);
          if (values.parent == null) {
            values.parent = ''
          }
          saveProductCategory(values);
        }}
      >
        {({ handleSubmit, setFieldValue, values }) => (
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
                {/* Parent Select */}
                <div className="col-lg-6">
                  <label>Parent</label>
                  <Field
                    name="parent"
                    component={({ field, form }) => (
                      <ReactSelect
                        isMulti={false}
                        options={parentOptions}
                        value={
                          parentOptions
                            ? parentOptions.find(
                                (option) => option.value === field.value
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
                </div>

                {/* Online Select */}
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

              <div className="form-group mb-2 row">
                <div className="col-lg-6">
                  <div className="row">
                    <div className=" col-lg-12 mb-2 form-group">
                      <label>Industry *</label>
                      <ReactSelect
                        isMulti
                        value={values.industry}
                        getOptionLabel={(option) => option.name}
                        getOptionValue={(option) => option.id}
                        onChange={(value) => {
                          setFieldValue("industry", value);
                        }}
                        name="industry"
                        options={industryList}
                        className="basic-multi-select"
                        classNamePrefix="select"
                      />
                      <ErrorMessage name="industry">
                        {(msg) => <div style={{ color: "red" }}>{msg}</div>}
                      </ErrorMessage>
                    </div>
                    <div className="col-lg-12">
                      <label>Select File </label>
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
                      <ErrorMessage name="image">
                        {(msg) => <div style={{ color: "red" }}>{msg}</div>}
                      </ErrorMessage>
                    </div>
                  </div>
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
                  ) : productCategory.image !== "" ? (
                    <img
                      className="ml-auto"
                      height="150"
                      width="300"
                      src={productCategory.image}
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
