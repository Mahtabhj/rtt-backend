import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import PropTypes from "prop-types";
import { toast } from "react-toastify";

import { uploadExemptions } from "../../../_redux/exemption/exemptionActions";
import { exemptionActionsLoading } from "../../../_redux/exemption/exemptionSelectors";

import { UploadModal } from "@common/UploadModal/UploadModal";

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  closeModalCallback: PropTypes.func.isRequired,
}

export const ExemptionUploadModal = ({ isModalShown, closeModalCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(exemptionActionsLoading);

  const [file, setFile] = useState(null);

  const handleOnClickSubmit = () => {
    if (file) {
      dispatch(uploadExemptions(file)).then(() => {
        setFile(null);
        closeModalCallback();
      });
    } else {
      toast.info('Add exemptions excel');
    }
  };

  const handleOnHide = () => closeModalCallback();

  return (
    <UploadModal
      title='Add Exemptions'
      isModalShown={isModalShown}
      file={file}
      setFile={setFile}
      onClose={handleOnHide}
      onSubmit={handleOnClickSubmit}
      actionsLoading={actionsLoading}
    />
  );
}

ExemptionUploadModal.propTypes = propTypes;
