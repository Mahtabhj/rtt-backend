import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import PropTypes from "prop-types";
import { toast } from "react-toastify";

import { uploadLimits } from "../../../_redux/limit/limitActions";
import { limitActionsLoading } from "../../../_redux/limit/limitSelectors";

import { UploadModal } from "@common/UploadModal/UploadModal";

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  closeModalCallback: PropTypes.func.isRequired,
}

export const LimitUploadModal = ({ isModalShown, closeModalCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(limitActionsLoading);

  const [file, setFile] = useState(null);

  const handleOnClickSubmit = () => {
    if (file) {
      dispatch(uploadLimits(file)).then(() => {
        setFile(null);
        closeModalCallback();
      });
    } else {
      toast.info('Add substances excel');
    }
  };

  const handleOnHide = () => closeModalCallback();

  return (
    <UploadModal
      title='Add Limits'
      isModalShown={isModalShown}
      file={file}
      setFile={setFile}
      onClose={handleOnHide}
      onSubmit={handleOnClickSubmit}
      actionsLoading={actionsLoading}
    />
  );
}

LimitUploadModal.propTypes = propTypes;
