import React, { useMemo, useState, useEffect } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from "@metronic-partials/controls";
import * as actions from "@redux-document/document/documentActions";
import * as regulation_actions from "@redux-regulation/regulation/regulationActions";
import { DocumentTable } from "./document-table/DocumentTable";
import FilterModal from "./FilterModal";
import { useDocumentUIContext } from "./DocumentUIContext";

import { useDispatch } from "react-redux";

export function DocumentCard() {
  const documentUIContext = useDocumentUIContext();
  const documentUIProps = useMemo(() => {
    return {
      ids: documentUIContext.ids,
      queryParams: documentUIContext.queryParams,
      setQueryParams: documentUIContext.setQueryParams,
      newDocumentButtonClick: documentUIContext.newDocumentButtonClick,
      openDeleteDocumentsDialog: documentUIContext.openDeleteDocumentsDialog,
      openEditDocumentPage: documentUIContext.openEditDocumentPage,
      openSelectDocumentPage: documentUIContext.openSelectDocumentPage,
      openUpdateDocumentStatusDialog:
        documentUIContext.openUpdateDocumentStatusDialog,
      openFetchDocumentDialog: documentUIContext.openFetchDocumentDialog,
    };
  }, [documentUIContext]);

  const [filterModalShow, setFilterModalShow] = useState(false);
  const [filter, setFilter] = useState(null);
  const [regulation, setRegulation] = useState([]);
  const [type, setType] = useState("");
  const [searchValue, setSearchvalue] = useState("");

  const handleClose = (filter, clicked = false) => {
    if (clicked) {
      const regulation =
        filter.regulations && filter.regulations.map((value) => value.id);
      setRegulation(regulation && regulation.join(","));
      const type = filter.types && filter.types.id;
      setType(type);
      setFilterModalShow(false);
    } else {
      setFilterModalShow(false);
    }
  };
  const handleShow = () => setFilterModalShow(true);

  const emptyFilter = () => {
    setRegulation(null);
    setType(null);
    setFilter(null);
    setSearchvalue(null);
    document.getElementById("search").value = "";
    sessionStorage.removeItem("dc_filter");
  };
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(
      actions.fetchDocumentList({
        search: searchValue,
        type: type,
        regulation_documents: regulation,
      })
    );
    dispatch(actions.fetchDocumentTypeList());
    dispatch(regulation_actions.fetchRegulationList());

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchValue, dispatch, regulation, type]);

  return (
    <Card>
      <CardHeader title="Document List">
        <CardHeaderToolbar>
          <button
            type="button"
            className="btn btn-primary"
            onClick={documentUIProps.newDocumentButtonClick}
          >
            Create Document{" "}
          </button>
        </CardHeaderToolbar>
      </CardHeader>

      <CardBody>
        <div className="d-flex justify-content-between flex-wrap">
          <div className="form-group">
            <input
              id="search"
              type="text"
              className="form-control"
              placeholder="Search..."
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  let value = e.target.value;
                  setSearchvalue(value);
                }
              }}
            />
          </div>
          <div className="popup">
            <FilterModal
              filterModalShow={filterModalShow}
              handleShow={handleShow}
              handleClose={handleClose}
              clearFilter={emptyFilter}
              setFilter={setFilter}
              filter={filter}
            />
          </div>
        </div>
        {documentUIProps.ids.length > 0 && <>{/* <DocumentGrouping /> */}</>}
        <DocumentTable />
      </CardBody>
    </Card>
  );
}
