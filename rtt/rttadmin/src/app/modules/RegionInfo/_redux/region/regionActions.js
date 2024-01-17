import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';

import * as RegionAPI from './regionApiService';

export const getRegions = createAsyncThunk(
	'region/getAll',
	async (_, { rejectWithValue }) => {
		try {
			const response = await RegionAPI.getRegions();
			return response.data;
		} catch (err) {
			toast.error(err.response.data?.message || 'Can not get regions list');
			return rejectWithValue(err.response.data?.error);
		}
	},
);