import React, { useState } from "react";
import { Button, Modal } from "react-bootstrap";
import PropTypes from "prop-types";
import { Formik } from "formik";
import dayjs from "dayjs";
import * as Yup from "yup";

import { DatePickerField } from "@metronic-partials/controls";
import { useDispatch } from "react-redux";

const ImportSchema = Yup.object().shape({
  from_date: Yup.string()
    .ensure()
    .required("Start is required"),
});

const propTypes = {
  title: PropTypes.string.isRequired,
  actionImport: PropTypes.func.isRequired,
  actionsLoading: PropTypes.bool,
}

export function ImportModal({ title, actionImport, actionsLoading }) {
  const dispatch = useDispatch();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOnClickOpen = () => setIsModalOpen(true);
  const handleOnClickClose = () => setIsModalOpen(false);

  const handleOnSubmit = ({ from_date }) => {
    const fromDate = dayjs(from_date).format('YYYY-MM-DD')

    dispatch(actionImport(fromDate)).then((res) => {
      setTimeout(() => {
        setIsModalOpen(res.status !== 200);
      },400);
    });
  };

  return (
    <>
      <Button variant="primary ml-2" onClick={handleOnClickOpen}>
        Import {title}
      </Button>

      <Modal show={isModalOpen} onHide={handleOnClickClose} size="sm">
        <Formik
          initialValues={{ from_date: dayjs().format("MM/DD/YYYY") }}
          validationSchema={ImportSchema}
          onSubmit={handleOnSubmit}
        >
          {({ handleSubmit }) => (
            <>
              <Modal.Header closeButton>
                <Modal.Title>Import {title}</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                <div className="form-group row">
                  <div className="col-auto">
                    <DatePickerField name="from_date" label="From Date *"/>
                  </div>
                </div>
              </Modal.Body>
              <Modal.Footer>
                <Button
                  onClick={handleOnClickClose}
                  className="btn btn-light btn-elevate"
                >
                  Close
                </Button>
                <Button
                  disabled={actionsLoading}
                  onClick={handleSubmit}
                  style={{ width: '100px' }}
                  className="btn btn-primary btn-elevate"
                >
                  Done
                  {actionsLoading && (<span className="ml-1 spinner spinner-white"/>)}
                </Button>
              </Modal.Footer>
            </>
          )}
        </Formik>
      </Modal>
    </>
  );
}

ImportModal.propTypes = propTypes;
