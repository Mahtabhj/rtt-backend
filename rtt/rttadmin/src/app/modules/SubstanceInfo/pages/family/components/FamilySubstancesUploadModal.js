import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';
import { toast } from 'react-toastify';

import { uploadFamilySubstances } from '../../../_redux/family/familyActions';
import { familyActionsLoading } from '../../../_redux/family/familySelectors';

import { ACTION_TYPE } from '@common';
import { UploadModal } from '@common/UploadModal/UploadModal';

const propTypes = {
  family: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
  }).isRequired,
  isModalShown: PropTypes.bool.isRequired,
  closeModalCallback: PropTypes.func.isRequired,
};

export const FamilySubstancesUploadModal = ({ family, isModalShown, closeModalCallback }) => {
  const dispatch = useDispatch();

  const actionsLoading = useSelector(familyActionsLoading);

  const [file, setFile] = useState(null);

  const handleOnClickSubmit = () => {
    if (file) {
      const dataToSend = {
        file,
        familyId: family.id,
      };

      dispatch(uploadFamilySubstances(dataToSend)).then((response) => {
        // check on wrong file format issue!
        if (!response?.type.endsWith(ACTION_TYPE.REJECTED)) {
          setFile(null);
          closeModalCallback();
        }
      });
    } else {
      toast.info('Add substances excel');
    }
  };

  const handleOnHide = () => closeModalCallback();

  return (
    <UploadModal
      title={`Add Substances to a Family: ${family.name}`}
      isModalShown={isModalShown}
      file={file}
      setFile={setFile}
      onClose={handleOnHide}
      onSubmit={handleOnClickSubmit}
      actionsLoading={actionsLoading}
    />
  );
};

FamilySubstancesUploadModal.propTypes = propTypes;
