import React from 'react';
import { useSelector } from 'react-redux';

import { regionIsLoading } from '../../_redux/region/regionSelectors';

import { LoadingDialog } from '@metronic-partials/controls';

import { RegionCard } from './RegionCard';

export const RegionPage = () => {
	const isLoading = useSelector(regionIsLoading);

	return (
		<>
			<LoadingDialog isLoading={isLoading} text="Loading ..." />

			<RegionCard />
		</>
	);
}
