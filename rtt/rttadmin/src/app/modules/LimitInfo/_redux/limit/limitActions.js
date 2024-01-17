import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from "react-toastify";

import * as LimitAPI from "./limitApiService";
import { limitSelector } from "./limitSelectors";

export const addLimit = createAsyncThunk(
  'limit/add',
  async (dataToSend, { rejectWithValue }) => {
    try {
      const response = await LimitAPI.addLimit(dataToSend);
      toast.success(response.data.message)
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);

export const editLimits = createAsyncThunk(
  'limit/edit',
  async (dataToSend, { rejectWithValue }) => {
    try {
      const response = await LimitAPI.updateLimit(dataToSend);
      toast.success(response.data.message)
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);

export const deleteLimits = createAsyncThunk(
  'limit/delete',
  async ({ ...dataToSend }, { rejectWithValue }) => {
    try {
      const response = await LimitAPI.deleteLimit(dataToSend);
      toast.success(response.data.message)
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);

export const uploadLimits = createAsyncThunk(
  'limit/upload',
  async (file, { rejectWithValue }) => {
    try {
      const response = await LimitAPI.uploadLimits(file);
      toast.success(response.data.message)
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);

export const getLimitForEdit = createAsyncThunk(
  'limit/getForEdit',
  async (id, { getState }) => {
    const state = getState();
    const limitsList = limitSelector(state);

    return await limitsList.results.find(limit => limit.id === id);
  },
);

export const getAllLimits = createAsyncThunk(
  'limit/getAll',
  async (queryParams, { rejectWithValue }) => {
    try {
      const response = await LimitAPI.getLimitsList(queryParams);
      return response.data;
    } catch (e) {
      return rejectWithValue("Can not get limit list")
    }
  },
);

export const getLimitFilteredIds = createAsyncThunk(
  'limit/getIds',
  async (queryParams, { rejectWithValue }) => {
    try {
      const response = await LimitAPI.getFilteredLimitsIdsList(queryParams);
      return response.data;
    } catch (e) {
      return rejectWithValue("Can not get limit list")
    }
  },
);

export const getLimitAttributes = createAsyncThunk(
  'limit/getAttributes',
  async (queryParams, { rejectWithValue }) => {
    try {
      const response = await LimitAPI.getLimitAttributesList(queryParams);
      return response.data;
    } catch (e) {
      return rejectWithValue("Can not get limit attributes")
    }
  },
);