import {
  getHandlerTableChange,
  getSelectRow,
  NoRecordsFoundMessage,
  pageListRenderer,
  PleaseWaitMessage,
} from "@metronic-helpers";
import * as actions from "@redux-product/product-category/productCategoryActions";
import React, { useEffect, useMemo } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { useProductCategoryUIContext } from "../ProductCategoryUIContext";
import * as uiHelpers from "../ProductCategoryUIHelpers";
import * as columnFormatters from "./column-formatters";

export function ProductCategoryTable({ filter, search }) {
  const productCategoryUIContext = useProductCategoryUIContext();

  const productCategoryUIProps = useMemo(() => {
    return {
      ids: productCategoryUIContext.ids,
      setIds: productCategoryUIContext.setIds,
      queryParams: productCategoryUIContext.queryParams,
      setQueryParams: productCategoryUIContext.setQueryParams,
      openEditProductCategoryPage:
        productCategoryUIContext.openEditProductCategoryPage,
      openSelectProductCategoryPage:
        productCategoryUIContext.openSelectProductCategoryPage,
      openDeleteProductCategoryDialog:
        productCategoryUIContext.openDeleteProductCategoryDialog,
    };
  }, [productCategoryUIContext]);

  // Getting curret state of productCategory list from store (Redux)
  const { currentState } = useSelector(
    (state) => ({ currentState: state.productCategory }),
    shallowEqual
  );

  const { totalCount, entities } = currentState;
  const dispatch = useDispatch();

  useEffect(() => {
    productCategoryUIProps.setIds([]);

    dispatch(
      actions.fetchProductCategoryList({
        ...productCategoryUIProps.queryParams,
        industry: filter,
        search: search,
      })
    );

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [productCategoryUIProps.queryParams, dispatch, filter, search]);

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
        openEditProductCategoryPage:
          productCategoryUIProps.openEditProductCategoryPage,
        openDeleteProductCategoryDialog:
          productCategoryUIProps.openDeleteProductCategoryDialog,
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
              bootstrap4
              remote
              bordered={false}
              keyField="id"
              data={entities === null ? [] : entities}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={getHandlerTableChange(
                productCategoryUIProps.setQueryParams
              )}
              selectRow={getSelectRow({
                entities,
                ids: productCategoryUIProps.ids,
                setIds: productCategoryUIProps.setIds,
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
