import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';

import * as SubstanceDataAPI from './substanceDataApiService';
import { substanceDataSelector } from './substanceDataSelectors';

export const addSubstanceData = createAsyncThunk(
  'substanceData/add',
  async (dataToSend, { rejectWithValue }) => {
    try {
      const response = await SubstanceDataAPI.addSubstanceData(dataToSend);
      return response.data?.message
    } catch (err) {
      return rejectWithValue(err.response.data?.error);
    }
  },
);

export const editSubstanceData = createAsyncThunk(
  'substanceData/edit',
  async ({ editPointId, ...dataToSend }, { rejectWithValue }) => {
    try {
      const response = await SubstanceDataAPI.updateSubstanceData(editPointId, dataToSend);
      return response.data?.message
    } catch (err) {
      return rejectWithValue(err.response.data?.error);
    }
  },
);

export const deleteSubstanceData = createAsyncThunk(
  'substanceData/delete',
  async (dataToSend, { rejectWithValue }) => {
    try {
      const response = await SubstanceDataAPI.deleteSubstanceData(dataToSend);
      toast.success(response.data?.message);
    } catch (err) {
      toast.error(err.response.data?.message || 'Something went wrong')
      return rejectWithValue(err.response.data?.error);
    }
  },
);

export const uploadSubstanceData = createAsyncThunk(
  'substanceData/upload',
  async (file, { rejectWithValue }) => {
    try {
      const response = await SubstanceDataAPI.uploadSubstanceData(file);
      toast.success(response.data?.message)
    } catch (err) {
      toast.error(err.response.data?.message || 'Something went wrong')
      return rejectWithValue(err.response.data?.error);
    }
  },
);

export const getSubstanceDataForEdit = createAsyncThunk(
  'substanceData/getForEdit',
  async (id, { getState }) => {
    const state = getState();
    const substanceDataList = substanceDataSelector(state);

    return await substanceDataList.results.find(substanceData => substanceData.id === id);
  },
);

export const getAllSubstanceData = createAsyncThunk(
  'substanceData/getAll',
  async (queryParams, { rejectWithValue }) => {
    try {
      const response = await SubstanceDataAPI.getSubstanceData(queryParams);
      return response.data;
    } catch (e) {
      return rejectWithValue("Can not get substance list")
    }
  },
);

export const getSubstanceDataFilteredIds = createAsyncThunk(
  'substanceData/getIds',
  async (queryParams, { rejectWithValue }) => {
    try {
      const response = await SubstanceDataAPI.getFilteredSubstanceDataIdsList(queryParams);
      return response.data;
    } catch (e) {
      return rejectWithValue("Can not get substance list")
    }
  },
);

export const getExistingSubstanceDataPoints = createAsyncThunk(
  'substanceData/getExistingPoints',
  async (dataToSend, { rejectWithValue }) => {
    try {
      const response = await SubstanceDataAPI.getExistingPoints(dataToSend);
      return response.data
        .map(({ id, name, substance_property_data_point }) => ({ name, ...substance_property_data_point, property_data_point: id }))
        .sort(({ id }) => id ? -1 : 0);
    } catch (e) {
      return rejectWithValue("Can not get existing substance data points")
    }
  },
);

export const getProperties = createAsyncThunk(
  'substanceData/getProperties',
  async (_, { rejectWithValue }) => {
    try {
      const response = await SubstanceDataAPI.getPropertyList();
      return response.data;
    } catch (e) {
      return rejectWithValue("Can not get properties")
    }
  },
);