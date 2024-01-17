import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import SVG from 'react-inlinesvg';

import { getRegions } from '../../_redux/region/regionActions';
import { regionSelector } from '../../_redux/region/regionSelectors';

import { Card, CardBody, CardHeader } from '@metronic-partials/controls';
import { headerFormatter, toAbsoluteUrl } from "@metronic-helpers";

import { RegionTable } from './region-table/RegionTable';

const firstColumnSticky = {
	backgroundColor: '#FFFFFF',
	position: 'sticky',
	left: 0,
	top: 0,
	zIndex: 1,
	borderRight: '1px solid #EBEDF3',
};

export const RegionCard = () => {
	const dispatch = useDispatch();

	const [tableColumns, setTableColumns] = useState([]);

	const { industries, regions } = useSelector(regionSelector);

	useEffect(() => {
		dispatch(getRegions());
	}, [dispatch]);

	useEffect(() => {
		const columns = [
			{
				dataField: 'name',
				text: '',
				style: {
					textAlign: 'center',
					fontWeight: 600,
					fontSize: '1rem',
					color: '#B5B5C3',
					...firstColumnSticky,
				},
				headerStyle: {
					...firstColumnSticky,
					zIndex: 2,
				},
				headerFormatter,
			},
			...industries.map(({ id, name }) => ({
				dataField: `${id}`,
				text: name,
				formatter: (_, { industries }) => {
					const { active_status: isActive } = industries.find(item => item.id === id) || {};

					return isActive ? <SVG src={toAbsoluteUrl(`${process.env.REACT_APP_STATIC_PATH}/svg/misc/Tick.svg`)} /> : null;
				},
				style: { textAlign: 'center', borderRight: '1px solid #EBEDF3' },
				headerFormatter,
				headerStyle: firstColumnSticky,
			})),
		];

		setTableColumns(columns);
	}, [industries])

	return (
		<Card>
			<CardHeader title="Region Data"></CardHeader>
			<CardBody>
				{!!regions.length && !!tableColumns.length && <RegionTable regions={regions} industries={tableColumns} />}
			</CardBody>
		</Card>
	)
}