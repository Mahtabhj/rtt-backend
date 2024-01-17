import React, { useState } from "react";
import { useSelector } from "react-redux";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider } from "react-bootstrap-table2-paginator";

import { NoRecordsFoundMessage, PleaseWaitMessage, pageListRenderer } from "@metronic-helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";

import * as uiHelpers from "../RegulationUIHelpers";
import * as columnFormatters from "./column-formatters";
import { UrlAddEditModal } from "./UrlAddEditModal";
import { UrlDeleteDialog } from "./UrlDeleteDialog";
import { UrlLinkUrlModal } from './UrlLinkUrlModal';

export function UrlTable({ regulationId }) {
  const regulationUrls = useSelector(state => state.regulation?.regulationForEdit?.urls || []);

  const [showUrlAddModal, setShowUrlAddModal] = useState(false);
  const [showUrlDeleteModal, setShowUrlDeleteModal] = useState(false);
  const [showLinkUrlModal, setShowLinkUrlModal] = useState(false);

  const [selectedUrlId, setSelectedUrl] = useState(null);
  const [selectedUrlIdDelete, setUrlIdDelete] = useState(null);

  const handleOpenLinkUrl = () => {
    setSelectedUrl(null);
    setShowLinkUrlModal(true);
  };

  const handleOpenAddUrlPage = () => {
    setSelectedUrl(null);
    setShowUrlAddModal(true);
  };

  const handleOpenEditUrlPage = id => {
    setSelectedUrl(id);
    setShowUrlAddModal(true);
  };

  const handleOpenDeleteUrlDialog = id => {
    setUrlIdDelete(id);
    setShowUrlDeleteModal(true);
  };

  // Table columns
  const columns = [
    {
      dataField: "id",
      text: "ID",
      sort: true,
    },
    {
      dataField: "text",
      text: "Text",
      sort: true,
      formatter: (cellContent) => (
        <div style={{ flex: 1, maxWidth: '420px'}}>
          <div style={{ textOverflow: 'ellipsis', whiteSpace: 'nowrap', overflow: 'hidden' }}>{cellContent}</div>
        </div>
      ),
    },
    {
      dataField: "description",
      text: "Description",
      sort: true,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditUrlPage: handleOpenEditUrlPage,
        openDeleteUrlDialog: handleOpenDeleteUrlDialog,
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  const paginationOptions = {
    totalSize: regulationUrls.length,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <Card>
        <CardHeader title="Urls List">
          <CardHeaderToolbar>
            <button
              style={{ marginRight: '10px' }}
              type="button"
              className="btn btn-primary"
              onClick={handleOpenLinkUrl}
            >
              Link Url
            </button>

            <button
              type="button"
              className="btn btn-primary"
              onClick={handleOpenAddUrlPage}
            >
              New Url
            </button>
          </CardHeaderToolbar>
        </CardHeader>

        <PaginationProvider pagination={paginationFactory(paginationOptions)}>
          {({ paginationTableProps }) => (
            <BootstrapTable
              wrapperClasses="table-responsive"
              classes="table table-head-custom table-vertical-center overflow-hidden"
              bootstrap4
              bordered={false}
              keyField="id"
              data={regulationUrls}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={() => null}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={regulationUrls} />
              <NoRecordsFoundMessage entities={regulationUrls} />
            </BootstrapTable>
          )}
        </PaginationProvider>
      </Card>

      <UrlLinkUrlModal
        setShowLinkUrlModal={setShowLinkUrlModal}
        regulationId={regulationId}
        showLinkUrlModal={showLinkUrlModal}
        idsOfSelectedUrls={regulationUrls.map(({ id }) => id)}
      />

      <UrlAddEditModal
        regulationId={regulationId}
        selectedUrlId={selectedUrlId}
        showUrlAddModal={showUrlAddModal}
        setShowUrlAddModal={setShowUrlAddModal}
      />

      <UrlDeleteDialog
        regulationId={regulationId}
        selectedUrlIdDelete={selectedUrlIdDelete}
        showUrlDeleteModal={showUrlDeleteModal}
        setShowUrlDeleteModal={setShowUrlDeleteModal}
      />
    </>
  );
}
