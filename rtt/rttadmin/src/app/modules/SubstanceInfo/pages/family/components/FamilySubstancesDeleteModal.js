import React from 'react';
import {useDispatch, useSelector} from 'react-redux';
import PropTypes from 'prop-types';

import { DeleteModal } from '@common';

import { familyActionsLoading } from '../../../_redux/family/familySelectors';
import { deleteFamilySubstance } from '../../../_redux/family/familyActions';

const propTypes = {
	familyId: PropTypes.number.isRequired,
	isModalShown: PropTypes.bool.isRequired,
	idsForDelete: PropTypes.arrayOf(PropTypes.number.isRequired).isRequired,
	closeModalCallback: PropTypes.func.isRequired,
	updateCallback: PropTypes.func.isRequired,
}

export const FamilySubstancesDeleteModal = ({ familyId, idsForDelete, isModalShown, closeModalCallback, updateCallback }) => {
	const dispatch = useDispatch();

	const actionsLoading = useSelector(familyActionsLoading);

	const submitDeleteSubstance = () => {
		const dataToSend = { id: familyId, substances: idsForDelete }

		dispatch(deleteFamilySubstance(dataToSend)).then(() => {
			updateCallback();
			closeModalCallback();
		})
	}

	return (
		<DeleteModal
			title={`Are you sure you want to remove the selected ${idsForDelete.length} Substances from this family?`}
			isModalShown={isModalShown}
			onClose={closeModalCallback}
			onSubmit={submitDeleteSubstance}
			actionsLoading={actionsLoading}
			actionButton="Remove"
			size="md"
		/>
	)
}

FamilySubstancesDeleteModal.propTypes = propTypes;