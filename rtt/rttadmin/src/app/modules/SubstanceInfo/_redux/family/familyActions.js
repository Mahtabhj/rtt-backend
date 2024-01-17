import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';

import * as FamilyAPI from './familyApiService';

export const addFamily = createAsyncThunk(
  'family/add',
  async (dataToSend, { rejectWithValue }) => {
    try {
      await FamilyAPI.addFamily(dataToSend);
      toast.success('Family added successfully');
    } catch (err) {
      toast.error(err.response.data?.error || 'Something went wrong');
      return rejectWithValue(err.response.data?.error);
    }
  }
);

export const getFamilyForEdit = createAsyncThunk(
  'family/getForEdit',
  async (id, { rejectWithValue }) => {
    try {
      const response = await FamilyAPI.getEditFamily(id);
      return response.data;
    } catch (err) {
      toast.error(err.response.data?.detail || 'Something went wrong');
      return rejectWithValue('Can not get family for edit');
    }
  }
);

export const editFamily = createAsyncThunk(
  'family/edit',
  async ({ id, ...dataToSend }, { rejectWithValue }) => {
    try {
      await FamilyAPI.updateFamily(id, dataToSend);
      toast.success('Family edited successfully');
    } catch (err) {
      toast.error(err.response.data?.error || 'Something went wrong');
      return rejectWithValue(err.response.data?.error);
    }
  }
);

export const deleteFamily = createAsyncThunk(
  'family/delete',
  async(id, { rejectWithValue }) => {
    try {
      const response = await FamilyAPI.deleteFamily(id);
      toast.success(response.data?.message);
    } catch (err) {
      toast.error(err.response.data?.message || 'Something went wrong');
      return rejectWithValue(err.response.data?.error);
    }
  }
);

export const getAllFamilies = createAsyncThunk(
  'family/getAll',
  async (queryParams, { rejectWithValue }) => {
    try {
      const response = await FamilyAPI.getFamilies(queryParams);
      return response.data;
    } catch (e) {
      return rejectWithValue('Can not get families list');
    }
  }
);

export const addFamilySubstances = createAsyncThunk(
  'family/addSubstances',
  async ({ id, substances }, { rejectWithValue }) => {
    try {
      const response = await FamilyAPI.addFamilySubstances(id, substances);
      toast.success(response.data?.message);
    } catch (err) {
      toast.error(err.response.data?.message || 'Something went wrong');
      return rejectWithValue(err.response.data?.error);
    }
  }
);

export const deleteFamilySubstance = createAsyncThunk(
  'family/deleteSubstances',
  async ({ id, substances }, { rejectWithValue }) => {
    try {
      const response = await FamilyAPI.deleteFamilySubstances(id, substances);
      toast.success(response.data?.message);
    } catch (err) {
      toast.error(err.response.data?.message || 'Something went wrong');
      return rejectWithValue(err.response.data?.error);
    }
  }
);

export const uploadFamilySubstances = createAsyncThunk(
  'family/uploadSubstances',
  async ({ file, familyId }, { rejectWithValue }) => {
    try {
      const response = await FamilyAPI.uploadFamilySubstances(file, familyId);
      toast.success(response.data?.message);
    } catch (err) {
      toast.error(err.response.data?.message || 'Something went wrong');
      return rejectWithValue(err.response.data?.error);
    }
  }
);

export const getFamilySubstances = createAsyncThunk(
  'family/getSubstances',
  async ({ id, ...dataToSend }, { rejectWithValue }) => {
    try {
      const response = await FamilyAPI.getSubstances(id, dataToSend);
      return response.data;
    } catch (e) {
      return rejectWithValue('Can not get family substances list');
    }
  }
);

export const getFamilySubstancesFilteredIds = createAsyncThunk(
  'family/getSubstancesIds',
  async ({ id, ...dataToSend }, { rejectWithValue }) => {
    try {
      const response = await FamilyAPI.getFilteredSubstancesIdsList(id, dataToSend);
      return response.data;
    } catch (e) {
      return rejectWithValue('Can not get family substances list');
    }
  }
);
