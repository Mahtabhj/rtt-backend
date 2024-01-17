import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import PropTypes from 'prop-types';
import { toast } from "react-toastify";
import { Modal } from "react-bootstrap";

import { addOrRemoveSubstancesManually, addSubstancesUpload } from "@redux/substances/substancesActions";

import { TabMenu, MANUAL_ADD, UPLOAD_FILE } from "@common";

import { AddSubstanceManual } from "./AddSubstanceManual";
import { UploadFile } from '../../UploadFile/UploadFile';

const propTypes = {
  updateCallback: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired,
};

export const AddSubstanceForm = ({ updateCallback, onClose }) => {
  const dispatch = useDispatch();

  const [selectedTab, setSelectedTab] = useState(MANUAL_ADD);

  const [chosenSubstances, setChosenSubstances] = useState([]);
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);

  const handleOnClickSubmit = () => {
    const afterSubmitAction = () => {
      updateCallback();
      onClose();
    };

    if (selectedTab === MANUAL_ADD) {
      const dataToSend = {
        substances: chosenSubstances.map(({ id }) => id),
        action: 'add',
      };

      if (dataToSend.substances.length) {
        dispatch(addOrRemoveSubstancesManually(dataToSend)).then(() => {
          afterSubmitAction();
        });
      } else {
        toast.info('Input substances');
      }
    } else {
      if (file) {
        dispatch(addSubstancesUpload(file, setProgress)).then(() => {
          afterSubmitAction();
        });
      } else {
        toast.info('Add substances excel');
      }
    }
  };

  return (
    <>
      <Modal.Body className="overlay overlay-block cursor-default">
        <TabMenu options={[MANUAL_ADD, UPLOAD_FILE]} selected={selectedTab} onSelect={setSelectedTab} />

        {selectedTab === MANUAL_ADD && (
          <div className="mt-5 mb-5">
            <AddSubstanceManual
              selected={chosenSubstances}
              onChange={setChosenSubstances}
              isValuesShown
            />
          </div>
        )}
        {selectedTab === UPLOAD_FILE && <UploadFile file={file} setFile={setFile} progress={progress} />}
      </Modal.Body>

      <Modal.Footer>
        <button
          type="button"
          onClick={onClose}
          className="btn btn-light btn-elevate"
        >
          Cancel
        </button>

        <button
          type="submit"
          onClick={handleOnClickSubmit}
          className="btn btn-primary btn-elevate"
        >
          Save
        </button>
      </Modal.Footer>
    </>
  );
};

AddSubstanceForm.propTypes = propTypes;
