import {
  getHandlerTableChange,
  getSelectRow,
  NoRecordsFoundMessage,
  pageListRenderer,
  PleaseWaitMessage,
} from "@metronic-helpers";
import * as actions from "@redux-product/material-category/materialCategoryActions";
import React, { useEffect, useMemo } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { useMaterialCategoryUIContext } from "../MaterialCategoryUIContext";
import * as uiHelpers from "../MaterialCategoryUIHelpers";
import * as columnFormatters from "./column-formatters";

export function MaterialCategoryTable() {
  // MaterialCategory UI Context
  const materialCategoryUIContext = useMaterialCategoryUIContext();

  const materialCategoryUIProps = useMemo(() => {
    return {
      ids: materialCategoryUIContext.ids,
      setIds: materialCategoryUIContext.setIds,
      queryParams: materialCategoryUIContext.queryParams,
      setQueryParams: materialCategoryUIContext.setQueryParams,
      openEditMaterialCategoryPage:
        materialCategoryUIContext.openEditMaterialCategoryPage,
      openSelectMaterialCategoryPage:
        materialCategoryUIContext.openSelectMaterialCategoryPage,
      openDeleteMaterialCategoryDialog:
        materialCategoryUIContext.openDeleteMaterialCategoryDialog,
    };
  }, [materialCategoryUIContext]);

  // Getting curret state of materialCategory list from store (Redux)
  const { currentState } = useSelector(
    (state) => ({ currentState: state.materialCategory }),
    shallowEqual
  );

  const { totalCount, entities } = currentState;

  // MaterialCategory Redux state
  const dispatch = useDispatch();

  useEffect(() => {
    // clear selections list
    materialCategoryUIProps.setIds([]);

    // server call by queryParams
    dispatch(
      actions.fetchMaterialCategoryList(materialCategoryUIProps.queryParams)
    );

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [materialCategoryUIProps.queryParams, dispatch]);

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },
    {
      dataField: "name",
      text: "Name",
      sort: true,
    },
    {
      dataField: "industry.name",
      text: "Industry",
      sort: true,
    },
    {
      dataField: "description",
      text: "Description",
      sort: true,
    },
    {
      dataField: "online",
      text: "Online",
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditMaterialCategoryPage:
          materialCategoryUIProps.openEditMaterialCategoryPage,
        openDeleteMaterialCategoryDialog:
          materialCategoryUIProps.openDeleteMaterialCategoryDialog,
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  // Table pagination properties
  const paginationOptions = {
    totalSize: totalCount,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <PaginationProvider pagination={paginationFactory(paginationOptions)}>
        {({ paginationProps, paginationTableProps }) => {
          return (
            <BootstrapTable
              wrapperClasses="table-responsive"
              classes="table table-head-custom table-vertical-center overflow-hidden"
              remote
              bootstrap4
              bordered={false}
              keyField="id"
              data={entities === null ? [] : entities}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={getHandlerTableChange(
                materialCategoryUIProps.setQueryParams
              )}
              selectRow={getSelectRow({
                entities,
                ids: materialCategoryUIProps.ids,
                setIds: materialCategoryUIProps.setIds,
              })}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={entities} />
              <NoRecordsFoundMessage entities={entities} />
            </BootstrapTable>
          );
        }}
      </PaginationProvider>
    </>
  );
}
