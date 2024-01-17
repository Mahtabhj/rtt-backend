import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';
import { toast } from 'react-toastify';

import { uploadSubstanceData } from '../../../_redux/substance-data/substanceDataActions';
import { substanceDataActionsLoading } from '../../../_redux/substance-data/substanceDataSelectors';

import { UploadModal } from '@common';

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  closeModalCallback: PropTypes.func.isRequired,
}

export const SubstanceDataUploadModal = ({ isModalShown, closeModalCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(substanceDataActionsLoading);

  const [file, setFile] = useState(null);

  const handleOnClickSubmit = () => {
    if (file) {
      dispatch(uploadSubstanceData(file)).then(() => {
        setFile(null);
        closeModalCallback();
      });
    } else {
      toast.info('Add substance data excel');
    }
  };

  const handleOnHide = () => closeModalCallback();

  return (
    <UploadModal
      title='Add Substance Data'
      isModalShown={isModalShown}
      file={file}
      setFile={setFile}
      onClose={handleOnHide}
      onSubmit={handleOnClickSubmit}
      actionsLoading={actionsLoading}
    />
  );
}

SubstanceDataUploadModal.propTypes = propTypes;
