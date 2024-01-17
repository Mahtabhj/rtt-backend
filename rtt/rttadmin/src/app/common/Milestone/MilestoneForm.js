import React, { useMemo } from "react";
import { Formik } from "formik";
import PropTypes from "prop-types";
import { Modal } from "react-bootstrap";
import * as Yup from "yup";
import dayjs from "dayjs";

import { MilestoneFieldsToEdit } from "./MilestoneFieldsToEdit";

// todo make common schemas
// Validation schema
const MilestoneEditSchema = Yup.object().shape({
  name: Yup.string()
    .min(3, "Minimum 3 symbols")
    .max(200, "Maximum 200 symbols")
    .required("Name is required"),
  from_date: Yup.string()
    .ensure()
    .required("Start is required"),
  to_date: Yup.string()
    .ensure()
    .required("End is required"),
  type: Yup.object().required("Type is required"),
  description: Yup.object().required("Description is required"),
});

const propTypes = {
  type: PropTypes.oneOf(['regulation', 'regulatoryFramework']).isRequired,
  milestone: PropTypes.object.isRequired,
  actionsLoading: PropTypes.bool.isRequired,
  setShowMilestoneAddModal: PropTypes.func.isRequired,
  saveRelatedMilestone: PropTypes.func.isRequired,
  milestoneTypeList: PropTypes.array.isRequired,
  documents: PropTypes.array.isRequired,
  urls: PropTypes.array.isRequired,
}

export function MilestoneForm(
  {
    type,
    milestone,
    actionsLoading,
    setShowMilestoneAddModal,
    saveRelatedMilestone,
    milestoneTypeList,
    documents,
    urls,
  }
) {
  const formattedTypes = useMemo(() =>
    milestoneTypeList.map(({ id, name }) => ({ title: name, value: id }))
  , [milestoneTypeList]);

  const selectedType = useMemo(() =>
      formattedTypes.find((type) => type.value === milestone.type)
  , [formattedTypes, milestone?.type])

  const milestoneForEdit = useMemo(() => {
    return ({ ...milestone, type: selectedType })
  }, [milestone, selectedType]);

  const handleOnClickCancel = () => setShowMilestoneAddModal();

  const handleOnSubmit = values => {
    const valuesToSend = { ...values };

    valuesToSend.from_date = dayjs(valuesToSend.from_date).format('YYYY-MM-DD').concat('T00:00:00');
    valuesToSend.to_date = dayjs(values.to_date).format('YYYY-MM-DD').concat('T00:00:00');

    valuesToSend.type = valuesToSend.type.value;
    valuesToSend.documents = valuesToSend.documents.map(({ id }) => id);
    valuesToSend.urls = valuesToSend.urls.map(({ id }) => id);
    delete valuesToSend.substances;

    saveRelatedMilestone(valuesToSend);
  };

  return (
    <Formik
      enableReinitialize
      initialValues={milestoneForEdit}
      validationSchema={MilestoneEditSchema}
      onSubmit={handleOnSubmit}
    >
      {({ handleSubmit, setFieldValue, values }) => (
        <>
          <Modal.Body className="overlay overlay-block cursor-default">
            {actionsLoading && (
              <div className="overlay-layer bg-transparent">
                <div className="spinner spinner-lg spinner-success"/>
              </div>
            )}
            <MilestoneFieldsToEdit
              id={milestoneForEdit.id}
              type={type}
              values={values}
              setFieldValue={setFieldValue}
              types={formattedTypes}
              documents={documents}
              urls={urls}
            />
          </Modal.Body>
          <Modal.Footer>
            <button
              className="btn btn-light btn-elevate"
              type="button"
              onClick={handleOnClickCancel}
            >
              Cancel
            </button>

            <button
              className="btn btn-primary btn-elevate"
              type="submit"
              onClick={() => handleSubmit()}
            >
              Save
            </button>
          </Modal.Footer>
        </>
      )}
    </Formik>
  );
}

MilestoneForm.propTypes = propTypes;
