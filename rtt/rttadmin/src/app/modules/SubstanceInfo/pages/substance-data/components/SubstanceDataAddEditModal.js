import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { Modal } from 'react-bootstrap';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import dayjs from 'dayjs';

import { ModalProgressBar } from '@metronic-partials/controls';

import {
  addSubstanceData,
  deleteSubstanceData,
  editSubstanceData,
  getExistingSubstanceDataPoints,
  getSubstanceDataForEdit,
} from '../../../_redux/substance-data/substanceDataActions';

import { SubstanceDataForm } from './SubstanceDataForm';

const initialSubstanceData = {
  substance: null,
  property: null,
  property_data_points: [],
};

const propTypes = {
  isModalShown: PropTypes.bool.isRequired,
  idForEdit: PropTypes.number,
  closeModalCallback: PropTypes.func.isRequired,
  updateCallback: PropTypes.func.isRequired,
};

const defaultProps = {
  idForEdit: null,
};

export const SubstanceDataAddEditModal = ({ isModalShown, idForEdit, closeModalCallback, updateCallback }) => {
  const dispatch = useDispatch();

  const [isLoading, setLoading] = useState(false);
  const [substanceData, setSubstanceData] = useState(initialSubstanceData);

  useEffect(() => {
    if (idForEdit) {
      setLoading(true);

      dispatch(getSubstanceDataForEdit(idForEdit)).then(({ payload: { substance, property } }) => {
        dispatch(getExistingSubstanceDataPoints({ substance: substance.id, property: property.id })).then(
          ({ payload: existingDataPoints }) => {
            const duplicatePointIds = existingDataPoints
              .map(({ property_data_point }) => property_data_point)
              .filter((item, index, self) => self.indexOf(item) === index && self.lastIndexOf(item) !== index);

            const filterDuplicatedItems = ({ id, property_data_point, status }, _, self) => {
              const getPossibleId = () => {
                const dataPointDuplicates = self.filter(item => item.property_data_point === property_data_point);

                const possiblePointItems = dataPointDuplicates.find(item => item.status === 'active')
                  ? []
                  : dataPointDuplicates
                      .filter(item => item.property_data_point === property_data_point)
                      .sort(({ modified: dateA }, { modified: dateB }) => {
                        if (dateA === dateB) return 0;
                        return dateA < dateB ? 1 : -1;
                      });

                const openAsEditDataPoint = possiblePointItems.find(item => item.id === idForEdit);

                return (openAsEditDataPoint || possiblePointItems[0])?.id;
              };

              return !duplicatePointIds.includes(property_data_point) || status === 'active' || id === getPossibleId();
            };

            const newInitialSubstanceData = {
              substance,
              property,
              property_data_points: existingDataPoints
                .filter(filterDuplicatedItems)
                .map(({ id: editPointId, property_data_point: id, name, value, status, modified, image }) => ({
                  editPointId,
                  id,
                  name,
                  value,
                  status,
                  modified,
                  image,
                  isChecked: true,
                }))
                .sort(({ status }) => (status === 'active' ? -1 : 0))
                .sort(({ editPointId }) => (editPointId === idForEdit ? -1 : 0)),
            };

            setLoading(false);
            setSubstanceData(newInitialSubstanceData);
          },
        );
      });
    } else {
      setSubstanceData(initialSubstanceData);
    }
  }, [dispatch, idForEdit]);

  const saveSubstanceData = ({ substance, property_data_points }, isSaveAsNewVersion) => {
    setLoading(true);

    const afterActionCallback = () => {
      updateCallback();
      closeModalCallback();
      setLoading(false);
    };

    const addSubstancePropertyDataPoint = dataToSend => dispatch(addSubstanceData(dataToSend));
    const editSubstancePropertyDataPoint = dataToSend => dispatch(editSubstanceData(dataToSend));
    const deleteSubstancePropertyDataPoints = dataToSend => dispatch(deleteSubstanceData(dataToSend));

    const prepareDataToSend = ({ id, value, status, modified, image }) => ({
      substance: substance?.id,
      property_data_point: id,
      value,
      status,
      modified: modified || dayjs().toISOString(),
      image,
    });

    const checkedPropertyDataPoints = property_data_points.filter(({ isChecked }) => isChecked);

    if (!checkedPropertyDataPoints.length) toast.info('There are no selected data points');

    const getRequestPromises = () =>
      checkedPropertyDataPoints.map(item => {
        // this item is editing
        if (item.editPointId) {
          if (isSaveAsNewVersion) {
            return addSubstancePropertyDataPoint(
              prepareDataToSend({ ...item, status: 'active', modified: dayjs().toISOString() }),
            );
          }

          return editSubstancePropertyDataPoint({ editPointId: item.editPointId, ...prepareDataToSend(item) });
        }

        return addSubstancePropertyDataPoint(prepareDataToSend(item));
      });

    const resolveAllPromises = () =>
      Promise.all(getRequestPromises()).then(responses => {
        const addedCount = responses.filter(({ type }) => type === 'substanceData/add/fulfilled').length;
        const editedCount = responses.filter(({ type }) => type === 'substanceData/edit/fulfilled').length;

        if (addedCount) {
          toast.success(`${addedCount} substance_data(s) have been added`);
        }
        if (editedCount) {
          toast.success(`${editedCount} substance_data(s) have been edited`);
        }

        afterActionCallback();
      });

    if (isSaveAsNewVersion) {
      deleteSubstancePropertyDataPoints({
        substance_data: checkedPropertyDataPoints
          .filter(({ editPointId }) => !!editPointId)
          .map(({ editPointId }) => editPointId),
      }).then(() => resolveAllPromises());
    } else {
      resolveAllPromises().then(() => {});
    }
  };

  const handleOnHide = () => closeModalCallback();

  const renderHeaderTitle = () => `${idForEdit ? 'Edit' : 'Add'} Substance Data`;

  return (
    isModalShown && (
      <Modal size="lg" show={isModalShown} onHide={handleOnHide} aria-labelledby="example-modal-sizes-title-lg">
        {isLoading && <ModalProgressBar variant="query" />}

        <Modal.Header>
          <Modal.Title id="example-modal-sizes-title-lg">{renderHeaderTitle()}</Modal.Title>
        </Modal.Header>

        <SubstanceDataForm
          substanceData={substanceData}
          saveSubstanceData={saveSubstanceData}
          onCancelCallback={closeModalCallback}
          isEdit={!!idForEdit}
          actionsLoading={isLoading}
        />
      </Modal>
    )
  );
};

SubstanceDataAddEditModal.propTypes = propTypes;
SubstanceDataAddEditModal.defaultProps = defaultProps;
