import React from "react";
import { Modal } from "react-bootstrap";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { Input, DatePickerField, Select } from "@metronic-partials/controls";

// Validation schema
const SubscriptionEditSchema = Yup.object().shape({
  start_date: Yup.mixed()
    .nullable(false)
    .required("Start date is required"),
  end_date: Yup.mixed()
    .nullable(false)
    .required("End Date is required"),
  max_user: Yup.number().required("Max user is required"),
});

export function SubscriptionForm({
  subscription,
  actionsLoading,
  setShowSubscriptionAddModal,
  saveOrganizationSubscription,
  organizationSubscriptionTypes,
}) {
  return (
    <>
      <Formik
        enableReinitialize={true}
        initialValues={subscription}
        validationSchema={SubscriptionEditSchema}
        onSubmit={(values) => {
          saveOrganizationSubscription(values);
        }}
      >
        {({ handleSubmit, errors }) => (
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
                    <DatePickerField name="start_date" label="Start Date *" />
                  </div>

                  <div className="col-lg-6">
                    <DatePickerField name="end_date" label="End Date *" />
                  </div>
                </div>

                <div className="form-group row">
                  <div className="col-lg-6">
                    <Select name="paid" label="Paid *">
                      <option key="Yes" value={true}>
                        Yes
                      </option>
                      <option key="No" value={false}>
                        No
                      </option>
                    </Select>
                  </div>

                  <div className="col-lg-6">
                    <Field
                      type="number"
                      name="amount"
                      component={Input}
                      placeholder="Amount"
                      label="Amount"
                    />
                  </div>
                </div>

                <div className="form-group row">
                  <div className="col-lg-6">
                    <Select
                      selected={
                        organizationSubscriptionTypes &&
                        organizationSubscriptionTypes.length > 0
                          ? organizationSubscriptionTypes[0].id
                          : null
                      }
                      name="type"
                      label="Type"
                    >
                      {organizationSubscriptionTypes.map((type, index) => (
                        <option key={type.id} value={type.id}>
                          {type.name}
                        </option>
                      ))}
                    </Select>
                    {errors.type ? (
                      <p style={{ color: "red" }}>{errors.type}</p>
                    ) : null}
                  </div>

                  <div className="col-lg-6">
                    <Field
                      type="number"
                      name="max_user"
                      component={Input}
                      placeholder="Max User"
                      label="Max User *"
                    />
                  </div>
                </div>
              </Form>
            </Modal.Body>
            <Modal.Footer>
              <button
                type="button"
                onClick={() => setShowSubscriptionAddModal(false)}
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
        )}
      </Formik>
    </>
  );
}
