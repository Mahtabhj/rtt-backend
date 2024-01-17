import React, { useMemo } from 'react';
import { useSelector } from 'react-redux';
import BootstrapTable from 'react-bootstrap-table-next';
import paginationFactory  from 'react-bootstrap-table2-paginator';

import {
  NoRecordsFoundMessage,
  PleaseWaitMessage,
  getHandlerTableChange,
  formatCategoriesNames,
  formatDateDDMMYYY,
  pageListRenderer
} from '@metronic-helpers';

import * as uiHelpers from '../ImpactAssessmentUIHelpers';
import { useImpactAssessmentUIContext } from '../ImpactAssessmentUIContext';
import { ActionsColumnFormatter } from './column-formatters/ActionsColumnFormatter';
import { SortCaret } from "../../../../../common/SortCaret/SortCaret";

export function ImpactAssessmentTable() {
  const impactAssessmentUIContext = useImpactAssessmentUIContext();

  const { setQueryParams, openSelectImpactAssessmentPage } = useMemo(() => {
    return {
      setQueryParams: impactAssessmentUIContext.setQueryParams,
      openSelectImpactAssessmentPage:
        impactAssessmentUIContext.openSelectImpactAssessmentPage,
    };
  }, [impactAssessmentUIContext]);

  const { totalCount, entities } = useSelector(state => state.newsImpactAssessment);

  // Table columns
  const columns = [
    {
      dataField: "news.pub_date",
      text: "Date",
      sort: true,
      sortCaret: order => <SortCaret order={order} />,
      formatter: cellContent => formatDateDDMMYYY(cellContent),
    },
    {
      dataField: "news.title",
      text: "Title",
    },
    {
      dataField: "news.source",
      text: "Source",
      formatter: cellContent => cellContent?.name,
    },
    {
      dataField: "organization.name",
      text: "Organization",
    },
    {
      dataField: "news.news_categories",
      text: "News categories",
      formatter: cellContent => formatCategoriesNames(cellContent),
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: ActionsColumnFormatter,
      formatExtraData: {
        openSelectImpactAssessmentPage,
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  const paginationOptions = {
    totalSize: totalCount,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <BootstrapTable
      wrapperClasses="table-responsive"
      classes="table table-head-custom table-vertical-center overflow-hidden"
      bootstrap4
      bordered={false}
      keyField="id"
      data={entities || []}
      columns={columns}
      pagination={paginationFactory(paginationOptions)}
      defaultSorted={uiHelpers.publicationDateSorted}
      onTableChange={getHandlerTableChange(setQueryParams)}
      remote
    >
      <PleaseWaitMessage entities={entities} />
      <NoRecordsFoundMessage entities={entities} />
    </BootstrapTable>
  );
}
