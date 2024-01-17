import React from 'react';
import SVG from 'react-inlinesvg';

import { toAbsoluteUrl } from './AssetsHelpers';

export const headerFormatter = ({ text }, colIndex, { filterElement /* , sortElement */ }) => (
  <div
    style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      minHeight: '50px',
    }}
  >
    <span>{text}</span>
    {filterElement}
    {/* {sortElement} */}
  </div>
);

/* Sorting Helpers */
export const sortCaret = (order /* , column */) => {
  if (!order)
    return (
      <span className="svg-icon svg-icon-sm svg-icon-primary ml-1 svg-icon-sort">
        <SVG src={toAbsoluteUrl('/media/svg/icons/Shopping/Sort1.svg')} />
      </span>
    );

  if (order === 'asc')
    return (
      <span className="svg-icon svg-icon-sm svg-icon-primary ml-1">
        <SVG src={toAbsoluteUrl('/media/svg/icons/Navigation/Up-2.svg')} />
      </span>
    );

  if (order === 'desc')
    return (
      <span className="svg-icon svg-icon-sm svg-icon-primary ml-1">
        <SVG src={toAbsoluteUrl('/media/svg/icons/Navigation/Down-2.svg')} />
      </span>
    );

  return null;
};

export const getPagesCount = (totalSize, sizePerPage) => Math.ceil(totalSize / sizePerPage);

export const getHandlerTableChange = setQueryParams => (
  type,
  { page, sizePerPage, sortField, sortOrder /* , data */ },
) => {
  const pageNumber = page || 1;

  setQueryParams(prev => {
    if (type === 'sort') return { ...prev, sortOrder, sortField };
    if (type === 'pagination') return { ...prev, pageNumber, pageSize: sizePerPage };
    return prev;
  });
};

export const PleaseWaitMessage = ({ entities }) => !entities && <div>Please wait...</div>;

export const NoRecordsFoundMessage = ({ entities }) => !!entities && !entities.length && <div>No records found</div>;

export const pageListRenderer = ({ pages, onPageChange }) => {
  const pageWithoutIndication = pages.filter(({ page }) => typeof page !== 'string'); // exclude <, <<, >>, >
  const getOnClickHandler = page => () => onPageChange(page);

  return (
    <div className="position-absolute" style={{ right: '1rem' }}>
      {pageWithoutIndication.map(({ page }) => (
        <button
          key={page}
          className="btn btn-primary ml-1 pt-2 pb-2 pr-3 pl-3"
          onClick={getOnClickHandler(page)}
          type="button"
        >
          {page}
        </button>
      ))}
    </div>
  );
};
