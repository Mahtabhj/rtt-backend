import React, { useEffect, useRef, useState } from "react";
import { shallowEqual, useSelector } from "react-redux";
import ReactSelect from "react-select";
import BootstrapTable from "react-bootstrap-table-next";

import { NoRecordsFoundMessage, PleaseWaitMessage } from "@metronic-helpers";
// import * as uiHelpers from "../../RegulationUIHelpers";
import { linkColumnFormatter } from "./LinkColumnFormatter";
import { UrlAddEditModal } from "./UrlAddEditModal";
import PropTypes from "prop-types";

const propTypes = {
  type: PropTypes.oneOf(['regulation', 'regulatoryFramework']).isRequired,
  selectedUrls: PropTypes.array.isRequired,
  setSelectedUrls: PropTypes.func.isRequired,
  urlOptions: PropTypes.array.isRequired,
}

export const SelectUrl = (
  {
    type,
    selectedUrls,
    setSelectedUrls,
    urlOptions,
    setUpdatedUrl
  }
) => {
  const { lastAddedUrl  } = useSelector(
    (state) => ({
      lastAddedUrl: state[type].lastAddedUrl,
    }),
    shallowEqual
  );
  const refLastAddedUrl = useRef(null);

  const [showUrlAddModal, setShowUrlAddModal] = useState(false);
  const [urlIdToEdit, setUrlIdToEdit] = useState(null);

  useEffect(() => {
    if (lastAddedUrl && lastAddedUrl.id !== refLastAddedUrl.current?.id) {
      refLastAddedUrl.current = lastAddedUrl;

      const urls = !!selectedUrls.length ? selectedUrls : selectedUrls;
      const newSelectedUls = [...urls, lastAddedUrl];
      setSelectedUrls(newSelectedUls);
    }
  }, [refLastAddedUrl, lastAddedUrl, selectedUrls, selectedUrls]);


  const handleOnChangeSelectedUrls = url => {
    const arrayOfSelectedUrls = [...selectedUrls];
    const index = arrayOfSelectedUrls.findIndex(item => item.id === url.id);

    if (index < 0) {
      arrayOfSelectedUrls.push(url);
    }

    setSelectedUrls(arrayOfSelectedUrls);
  };

  const handleOnRemoveUrl = id => {
    const newSelectedUrls = selectedUrls.filter(url => url.id !== id);
    setSelectedUrls(newSelectedUrls);
  };

  const handleOnCloseUrlEditModal = () => {
    setShowUrlAddModal(false);
    setUrlIdToEdit(null);
  }

  const handleOnClickNewUrl = () => setShowUrlAddModal(true);

  const columnsUrls = [
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
      formatter: (cellContent) => (
        <div
          dangerouslySetInnerHTML={{ __html: cellContent }}
          style={{ maxHeight: '150px', overflow: 'hidden' }}
        />
      )
    },
    {
      dataField: "action",
      text: "Actions",
      formatter: linkColumnFormatter,
      formatExtraData: {
        openEditLinkPage: (id) => {
          setShowUrlAddModal(true);
          setUrlIdToEdit(id);
        },
        openDeleteLinkDialog: (id) => {
          handleOnRemoveUrl(id);
        },
      },
      classes: "text-right pr-0",
      headerClasses: "text-right pr-3",
      style: {
        minWidth: "100px",
      },
    },
  ];

  return (
    <>
      <div className="row flex align-items-end">
        <div className="col-lg-10">
          <label>Select Urls</label>
          <ReactSelect
            value={[]}
            getOptionLabel={(option) => option.description || option.text}
            getOptionValue={(option) => option.id}
            onChange={handleOnChangeSelectedUrls}
            name="urls"
            options={urlOptions}
            className="basic-multi-select"
            classNamePrefix="select"
          />
        </div>

        <button
          type="button"
          onClick={handleOnClickNewUrl}
          className="btn btn-primary btn-elevate"
        >
          New URL
        </button>
      </div>

      <BootstrapTable
        wrapperClasses="table-responsive"
        classes="table table-head-custom table-vertical-center overflow-hidden"
        bootstrap4
        bordered={false}
        keyField="id"
        data={selectedUrls || []}
        columns={columnsUrls}
        // defaultSorted={uiHelpers.defaultSorted}
      >
        <PleaseWaitMessage entities={selectedUrls || []} />
        <NoRecordsFoundMessage entities={selectedUrls || []} />
      </BootstrapTable>

      <UrlAddEditModal
        type={type}
        showUrlAddModal={showUrlAddModal}
        setShowUrlAddModal={handleOnCloseUrlEditModal}
        urlObject={urlOptions.find(url => url.id === urlIdToEdit)}
        setUpdatedUrl={setUpdatedUrl}
      />
    </>
  )
}

SelectUrl.propTypes = propTypes;
