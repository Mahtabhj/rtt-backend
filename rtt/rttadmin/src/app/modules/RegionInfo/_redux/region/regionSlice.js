import { createSlice } from '@reduxjs/toolkit';

import { getRegions } from './regionActions';

const initialState = {
	data: {
		industries: [],
		regions: [],
	},
	isLoading: false,
}

export const regionDataSlice = createSlice({
	name: 'region',
	initialState,
	reducers: {},
	extraReducers: builder => {
		builder
			.addCase(getRegions.fulfilled, (state, { payload }) => {
				state.data = payload;
			})
			.addMatcher(
				action => action.type.endsWith('pending'),
				(state) => {
					state.isLoading = true;
				}
			)
			.addMatcher(
				action => action.type.endsWith('fulfilled'),
				(state) => {
					state.isLoading = false;
				}
			)
			.addMatcher(
				action => action.type.endsWith('rejected'),
				(state) => {
					state.isLoading = false;
				}
			)
	},
})