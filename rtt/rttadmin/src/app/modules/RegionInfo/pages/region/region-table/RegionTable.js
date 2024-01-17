import React from 'react';
import PropTypes from 'prop-types';

import BootstrapTable from 'react-bootstrap-table-next';

import './style.scss';

const propTypes = {
	regions: PropTypes.arrayOf(PropTypes.shape({})).isRequired,
	industries: PropTypes.arrayOf(PropTypes.shape({})).isRequired,
};

export const RegionTable = ({ regions, industries }) => {
	return (
		<BootstrapTable
			wrapperClasses="table-responsive region-table"
			classes="table table-head-custom table-vertical-center"
			keyField="name"
			bordered={false}
			data={regions}
			columns={industries}
		/>
	)
}

RegionTable.propTypes = propTypes;