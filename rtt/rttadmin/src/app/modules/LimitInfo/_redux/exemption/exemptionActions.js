import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from "react-toastify";

import * as ExemptionAPI from "./exemptionApiService";
import { exemptionSelector } from "./exemptionSelectors";

export const addExemption = createAsyncThunk(
  'exemption/add',
  async ({ ...dataToSend }, { rejectWithValue }) => {
    try {
      const response = await ExemptionAPI.addExemption(dataToSend);
      toast.success(response.data.message || 'Exemption added successfully')
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);

export const editExemption = createAsyncThunk(
  'exemption/edit',
  async ({ id, ...dataToSend }, { rejectWithValue }) => {
    try {
      const response = await ExemptionAPI.updateExemption(id, dataToSend);
      toast.success(response.data.message || 'Exemption edited successfully');
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);

export const deleteExemptions = createAsyncThunk(
  'exemption/delete',
  async ({ ...dataToSend }, { rejectWithValue }) => {
    try {
      const response = await ExemptionAPI.deleteExemption(dataToSend);
      toast.success(response.data.message)
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);

export const uploadExemptions = createAsyncThunk(
  'exemption/upload',
  async (file, { rejectWithValue }) => {
    try {
      const response = await ExemptionAPI.uploadExemptions(file);
      toast.success(response.data.message)
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);

export const getExemptionForEdit = createAsyncThunk(
  'exemption/getForEdit',
  async (id, { getState }) => {
    const state = getState();
    const exemptionsList = exemptionSelector(state);

    return await exemptionsList.results.find(exemption => exemption.id === id);
  },
);

export const getAllExemption = createAsyncThunk(
  'exemption/getAll',
  async (queryParams, { rejectWithValue }) => {
    try {
      const response = await ExemptionAPI.getExemptionsList(queryParams);
      return response.data;
    } catch (e) {
      return rejectWithValue("Can not get exemption list")
    }
  },
);

export const getExemptionFilteredIds = createAsyncThunk(
  'exemption/getIds',
  async (queryParams, { rejectWithValue }) => {
    try {
      const response = await ExemptionAPI.getFilteredExemptionsIdsList(queryParams);
      return response.data;
    } catch (e) {
      return rejectWithValue("Can not get exemption list")
    }
  },
);