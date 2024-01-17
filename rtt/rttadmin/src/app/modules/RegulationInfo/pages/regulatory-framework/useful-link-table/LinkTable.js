import { NoRecordsFoundMessage, PleaseWaitMessage, pageListRenderer } from "@metronic-helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import React, { useState } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { useSelector } from "react-redux";
import * as uiHelpers from "../../regulatory-framework/RegulatoryFrameworkUIHelpers";
import * as columnFormatters from "./column-formatters";
import { LinkAddEditModal } from "./LinkAddEditModal";
import { LinkDeleteDialog } from "./LinkDeleteDialog";
import { LinkUrlModal } from './LinkUrlModal';

export function LinkTable({ regulatoryFrameworkId }) {
  const regulatoryFrameworkUrls = useSelector(({ regulatoryFramework }) => regulatoryFramework.regulatoryFrameworkForEdit?.urls || []);

  const [showLinkAddModal, setShowLinkAddModal] = useState(false);
  const [showLinkDeleteModal, setShowLinkDeleteModal] = useState(false);
  const [showLinkUrlModal, setShowLinkUrlModal] = useState(false);

  const [selectedLinkId, setSelectedLink] = useState(null);
  const [selectedLinkIdDelete, setLinkIdDelete] = useState(null);

  const handleOpenLinkUrl = () => {
    setSelectedLink(null);
    setShowLinkUrlModal(true);
  }

  const handleOpenAddLinkPage = () => {
    setSelectedLink(null);
    setShowLinkAddModal(true);
  };

  const handleOpenEditLinkPage = id => {
    setSelectedLink(id);
    setShowLinkAddModal(true);
  };

  const handleOpenDeleteLinkDialog = id => {
    setLinkIdDelete(id);
    setShowLinkDeleteModal(true);
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
        openEditLinkPage: handleOpenEditLinkPage,
        openDeleteLinkDialog: handleOpenDeleteLinkDialog,
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  const paginationOptions = {
    totalSize: regulatoryFrameworkUrls.length,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <Card>
        <CardHeader title="Links list">
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
              onClick={handleOpenAddLinkPage}
            >
              New Link
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
              data={regulatoryFrameworkUrls}
              columns={columns}
              defaultSorted={uiHelpers.defaultSorted}
              onTableChange={() => null}
              {...paginationTableProps}
            >
              <PleaseWaitMessage entities={regulatoryFrameworkUrls} />
              <NoRecordsFoundMessage entities={regulatoryFrameworkUrls} />
            </BootstrapTable>
          )}
        </PaginationProvider>
      </Card>

      <LinkAddEditModal
        regulatoryFrameworkId={regulatoryFrameworkId}
        selectedLinkId={selectedLinkId}
        showLinkAddModal={showLinkAddModal}
        setShowLinkAddModal={setShowLinkAddModal}
      />

      <LinkDeleteDialog
        regulatoryFrameworkId={regulatoryFrameworkId}
        selectedLinkIdDelete={selectedLinkIdDelete}
        showLinkDeleteModal={showLinkDeleteModal}
        setShowLinkDeleteModal={setShowLinkDeleteModal}
      />

      <LinkUrlModal
        setShowLinkUrlModal={setShowLinkUrlModal}
        regulatoryFrameworkId={regulatoryFrameworkId}
        showLinkUrlModal={showLinkUrlModal}
        idsOfSelectedUrls={regulatoryFrameworkUrls.map(({ id }) => id)}
      />
    </>
  );
}
