import React, { useEffect, useState } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import { useDispatch, useSelector } from "react-redux";
import * as actions from "@redux-regulation/regulatory-framework/regulatoryFrameworkActions";
import * as uiHelpers from "../../regulatory-framework/RegulatoryFrameworkUIHelpers";
import { NoRecordsFoundMessage, PleaseWaitMessage } from "@metronic-helpers";
import {
  Card,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";

import { MilestoneAddEditModal } from "@common/Milestone/MilestoneAddEditModal";
import { MilestoneDeleteDialog } from "./MilestoneDeleteDialog";

import * as columnFormatters from "./column-formatters";

export function MilestoneTable({ regulatoryFrameworkId }) {
  const dispatch = useDispatch();

  const { relatedMilestones } = useSelector((state) => ({ relatedMilestones: state.regulatoryFramework?.relatedMilestones }));

  const [isAddModalShown, setAddModalShown] = useState(false);
  const [isDeleteModalShown, setDeleteModalShown] = useState(false);

  const [selectedMilestoneId, setSelectedMilestone] = useState(null);
  const [selectedMilestoneIdDelete, setMilestoneIdDelete] = useState(null);

  const handleOnCloseMilestoneModal = () => {
    setAddModalShown(false);
    setSelectedMilestone(null);

    dispatch(actions.milestoneDropLastAttachmentsAction());
  };

  const handleOnClickNewMilestone = () => {
    setSelectedMilestone(null);
    setAddModalShown(true);
  };

  useEffect(() => {
    dispatch(actions.fetchRelatedMilestoneList(regulatoryFrameworkId));
  }, [regulatoryFrameworkId, dispatch]);

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
      dataField: "type",
      text: "Type",
      sort: true,
      formatter: (cellContent) => cellContent?.name,
    },
    {
      dataField: "from_date",
      text: "From Date",
      sort: true,
      formatter: columnFormatters.DateFormatter,
    },
    {
      dataField: "to_date",
      text: "To Date",
      sort: true,
      formatter: columnFormatters.DateFormatter,
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: columnFormatters.ActionsColumnFormatter,
      formatExtraData: {
        openEditMilestonePage: (id) => {
          setAddModalShown(true);
          setSelectedMilestone(id);
        },
        openDeleteMilestoneDialog: (id) => {
          setMilestoneIdDelete(id);
          setDeleteModalShown(true);
        },
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  const pageListRenderer = ({ pages, onPageChange }) => {
    // just exclude <, <<, >>, >
    const pageWithoutIndication = pages.filter(
      (p) => typeof p.page !== "string"
    );
    return (
      <div className="position-absolute" style={{ right: "1rem" }}>
        {pageWithoutIndication.map((p) => (
          <button
            className="btn btn-primary ml-1 pt-2 pb-2 pr-3 pl-3"
            onClick={() => onPageChange(p.page)}
            key={p.page}
          >
            {p.page}
          </button>
        ))}
      </div>
    );
  };

  const paginationOptions = {
    totalSize: relatedMilestones && relatedMilestones.length,
    sizePerPageList: uiHelpers.sizePerPageList,
    hideSizePerPage: false,
    hidePageListOnlyOnePage: false,
    pageListRenderer,
  };

  return (
    <>
      <Card>
        <CardHeader title="Milestones List">
          <CardHeaderToolbar>
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleOnClickNewMilestone}
            >
              New Milestone
            </button>
          </CardHeaderToolbar>
        </CardHeader>

        <PaginationProvider pagination={paginationFactory(paginationOptions)}>
          {({ paginationProps, paginationTableProps }) => {
            return (
              <BootstrapTable
                wrapperClasses="table-responsive"
                classes="table table-head-custom table-vertical-center overflow-hidden"
                bootstrap4
                bordered={false}
                keyField="id"
                data={relatedMilestones === undefined ? [] : relatedMilestones}
                columns={columns}
                onTableChange={() => null}
                {...paginationTableProps}
              >
                <PleaseWaitMessage entities={relatedMilestones} />
                <NoRecordsFoundMessage entities={relatedMilestones} />
              </BootstrapTable>
            );
          }}
        </PaginationProvider>
      </Card>
      <MilestoneAddEditModal
        type="regulatoryFramework"
        isModalShown={isAddModalShown}
        closeModalCallback={handleOnCloseMilestoneModal}
        regulationId={+regulatoryFrameworkId}
        selectedMilestoneId={selectedMilestoneId}
      />

      <MilestoneDeleteDialog
        regulatoryFrameworkId={regulatoryFrameworkId}
        selectedMilestoneIdDelete={selectedMilestoneIdDelete}
        showMilestoneDeleteModal={isDeleteModalShown}
        setShowMilestoneDeleteModal={setDeleteModalShown}
      />
    </>
  );
}
