import React from 'react';
import dayjs from 'dayjs';
import jwt_decode from 'jwt-decode';
import { toast } from 'react-toastify';

import { ShortNameTooltip } from '.';
import { DATE_FORMAT_FOR_REQUEST, DATE_FULL_YEAR_FORMAT, TITLE_LIMIT_SHORT } from './constants';

export const getBoolString = bool => (bool ? 'true' : 'false');

export const shortTitleLength = (title, limit) =>
  // 'limit - 3' to get a result of limited length ending in '...'
  title?.length > limit ? title.substring(0, limit - 3).concat('...') : title;

export const getCustomLabel = (option, isNameTooltip) => (
  <div className="d-flex justify-content-between w-100">
    {isNameTooltip ? (
      <ShortNameTooltip id={option.id} name={option.name} isAutoHide isModalTooltip />
    ) : (
      <span>{shortTitleLength(option.name, TITLE_LIMIT_SHORT)}</span>
    )}
    {!!option.regions?.length && <span className="ml-1">({option.regions.map(region => region.name).join(', ')})</span>}
    {!!option.region?.name && <span className="ml-1">({option.region?.name})</span>}
  </div>
);

export const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / k ** i).toFixed(dm))} ${sizes[i]}`;
};

export const getSuperuserKeyFromJwt = token => {
  if (!token) return false;

  const { is_superuser } = jwt_decode(token);
  return is_superuser; // return false to test permissions
};

export const formatDateFullYear = date => (date ? dayjs(date).format(DATE_FULL_YEAR_FORMAT) : null);
export const prepareDateForRequest = date => (date ? dayjs(date).format(DATE_FORMAT_FOR_REQUEST) : null);

export const isObject = item => !!item && typeof item === 'object' && !Array.isArray(item);

export const getNewsCategoriesTopicsIds = newsCategories =>
  newsCategories ? [...new Set(newsCategories.map(({ topic }) => topic?.id).filter(topicId => !!topicId))] : [];

const FIFTEEN_SECONDS = 15000;

export const toastInfoProlonged = message => toast.info(message, { autoClose: FIFTEEN_SECONDS });
