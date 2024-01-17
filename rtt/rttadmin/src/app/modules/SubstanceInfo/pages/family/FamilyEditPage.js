import React, { useEffect, useState, useCallback, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useHistory, useParams } from 'react-router-dom';

import { editFamily, getFamilyForEdit } from "../../_redux/family/familyActions";
import { familyActionsLoading } from '../../_redux/family/familySelectors';

import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
  ModalProgressBar
} from '@metronic-partials/controls';

import { BUTTON } from '@common';
import { UiKitButton } from '@common/UIKit';

import { FAMILY_TAB, SUBSTANCE_MAIN_PATH } from '../../SubstanceRoutes';
import { FamilyForm } from './components/FamilyForm';
import { FamilySubstances } from './components/FamilySubstances';
import { ACTION_TYPE } from "../../../../common";

const initialFamily = {
  id: null,
  chemycal_id: '',
  name: '',
  substances: [],
};

export function FamilyEditPage() {
  const btnRef = useRef();
  const { id } = useParams();
  const history = useHistory();
  const dispatch = useDispatch();

  const [family, setFamily] = useState(initialFamily);

  const actionsLoading = useSelector(familyActionsLoading);

  const backToFamilies = useCallback(() =>
      history.push(`${SUBSTANCE_MAIN_PATH}/${FAMILY_TAB}`)
    , [dispatch, history]);

  useEffect(() => {
    dispatch(getFamilyForEdit(id)).then(response => {
      if (!response?.type.endsWith(ACTION_TYPE.REJECTED)) {
        setFamily(response.payload);
      } else backToFamilies();
    });
  }, [id, dispatch, backToFamilies]);

  const saveFamily = useCallback(
    ({ id, name, chemycal_id }) =>
      dispatch(
        editFamily({
          id,
          name: name.trim(),
          chemycal_id: chemycal_id.trim(),
        })
      ).then(response => {
        if (!response?.type.endsWith(ACTION_TYPE.REJECTED)) {
          backToFamilies();
        }
      }),
    [dispatch, backToFamilies],
  );

  const saveFamilyClick = () => btnRef?.current && btnRef.current.click();

  return (
    <Card>
      {actionsLoading && <ModalProgressBar />}
      <CardHeader title="Edit Family">
        <CardHeaderToolbar>
          <button
            type="button"
            onClick={backToFamilies}
            className="btn btn-light mr-2"
          >
            <i className="fa fa-arrow-left" />
            Back
          </button>
          <UiKitButton buttonType={BUTTON.SAVE} onClick={saveFamilyClick} isLoading={actionsLoading} />
        </CardHeaderToolbar>
      </CardHeader>
      <CardBody>
        <FamilyForm
          family={family}
          saveFamily={saveFamily}
          onCancelCallback={backToFamilies}
          actionsLoading={actionsLoading}
          btnRef={btnRef}
        />

        {!!family.id && <FamilySubstances family={family} />}
      </CardBody>
    </Card>
  );
}
