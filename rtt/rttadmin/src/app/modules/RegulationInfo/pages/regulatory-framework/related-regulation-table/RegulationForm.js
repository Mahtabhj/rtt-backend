import React from 'react';
import { useSelector } from 'react-redux';
import { Modal } from 'react-bootstrap';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import RichTextEditor from 'react-rte';
import * as Yup from 'yup';

import { Input, Select } from '@metronic-partials/controls';
import { BUTTON } from '@common';
import { UiKitButton } from '@common/UIKit';

// Validation schema
const RegulationEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(1, 'Minimum 1 character')
    .max(200, 'Maximum 200 characters')
    .required('Name is required'),
  type: Yup.string()
    .ensure()
    .required('Regulation type is required'),
  status: Yup.string()
    .ensure()
    .required('Status is required'),
  review_status: Yup.string()
    .ensure()
    .required('Review status is required'),
  language: Yup.string()
    .ensure()
    .required('Language is required'),
});

export function RegulationForm({
  regulation,
  onSave,
  onCancel,
  actionsLoading,
  children
}) {
  const {
    currentState: {
      regulationTypeList,
      languageList,
      statusList,
    }
  } = useSelector(state => ({ currentState: state.regulatoryFramework }));

  return (
    <Formik
      enableReinitialize
      initialValues={{ ...regulation }}
      validationSchema={RegulationEditSchema}
      onSubmit={onSave}
    >
      {({ handleSubmit, setFieldValue, values, errors }) => (
        <>
          <Modal.Body className="overlay overlay-block cursor-default">
            <Form className="form form-label-right">
              <div className="form-group row">
                <div className="col-lg-6">
                  <Field
                    name="name"
                    component={Input}
                    placeholder="Name"
                    label="Name"
                    withFeedbackLabel={false}
                  />
                  {!!errors.name && (
                    <p className="text-danger"> {errors.name} </p>
                  )}
                </div>

                <div className="col-lg-6">
                  <Select
                    name="review_status"
                    label="Review Status"
                    withFeedbackLabel={false}
                  >
                    <option key="true" value={"d"}>
                      Draft
                    </option>
                    <option key="false" value={"o"}>
                      Online
                    </option>
                  </Select>
                  <ErrorMessage name="review_status">
                    {(msg) => <div className="text-danger">{msg}</div>}
                  </ErrorMessage>
                </div>
              </div>

              <div className="form-group row">
                <div className="col-lg-6">
                  <Select name="type" label="Type" withFeedbackLabel={false}>
                    {regulationTypeList.map((type, index) => (
                      <option
                        key={type.id}
                        value={regulationTypeList[index].id}
                      >
                        {type.name}
                      </option>
                    ))}
                  </Select>
                </div>
                <div className="col-lg-6">
                  <Select
                    name="language"
                    label="Language"
                    withFeedbackLabel={false}
                  >
                    {languageList.map((option, index) => (
                      <option key={option.id} value={languageList[index].id}>
                        {option.name}
                      </option>
                    ))}
                  </Select>
                  <ErrorMessage name="language">
                    {(msg) => <div className="text-danger">{msg}</div>}
                  </ErrorMessage>
                </div>
              </div>
              <div className="form-group row">
                <div className="col-lg-6">
                  <Select
                    name="status"
                    label="Status"
                    withFeedbackLabel={false}
                  >
                    {statusList.map((option, index) => (
                      <option key={option.id} value={statusList[index].id}>
                        {option.name}
                      </option>
                    ))}
                  </Select>
                  <ErrorMessage name="type">
                    {(msg) => <div style={{ color: "red" }}>{msg}</div>}
                  </ErrorMessage>
                </div>
              </div>

              <div className="form-group row">
                <div className="col-lg-12">
                  <label>Description</label>

                  <RichTextEditor
                    value={values.description}
                    onChange={(value) => setFieldValue("description", value)}
                  />
                </div>
              </div>

              <div className="form-group row">
                <div className="col-lg-12">
                  {children}
                </div>
              </div>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <UiKitButton buttonType={BUTTON.CANCEL} onClick={onCancel} isLoading={actionsLoading} />
            <UiKitButton buttonType={BUTTON.SAVE} onClick={handleSubmit} isLoading={actionsLoading}/>
          </Modal.Footer>
        </>
      )}
    </Formik>
  );
}
