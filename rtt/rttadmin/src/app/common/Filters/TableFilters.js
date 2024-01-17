import React from 'react';
import { customFilter } from 'react-bootstrap-table2-filter';

import { CheckboxesFilter, DateFilter, LimitFilter, SelectFilter, TextFilter } from '@common/Filters';

export const getTextFilter = () => ({
  filter: customFilter(),
  filterRenderer: onFilter => <TextFilter onSelect={onFilter} />,
});

export const getCheckboxesFilter = type => ({
  filter: customFilter(),
  filterRenderer: onFilter => <CheckboxesFilter onSelect={onFilter} type={type} />,
});

export const getDateFilter = () => ({
  filter: customFilter(),
  filterRenderer: onFilter => <DateFilter onSelect={onFilter} />,
});

export const getLimitFilter = () => ({
  filter: customFilter(),
  filterRenderer: onFilter => <LimitFilter onSelect={onFilter} />,
});

export const getStatusFilter = () => ({
  filter: customFilter(),
  filterRenderer: onFilter => <SelectFilter options={['active', 'deleted']} onSelect={onFilter} />,
});