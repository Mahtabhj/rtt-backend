/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-product/industry/industryActions";
import { useIndustryUIContext } from "../IndustryUIContext";

export function IndustryDeleteDialog({ id, show, onHide }) {
  // Industry UI Context
  const industryUIContext = useIndustryUIContext();
  const industryUIProps = useMemo(() => {
    return {
      setIds: industryUIContext.setIds,
      queryParams: industryUIContext.queryParams,
    };
  }, [industryUIContext]);

  // Industry Redux state
  const dispatch = useDispatch();
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.industry.actionsLoading }),
    shallowEqual
  );

  // if !id we should close modal
  useEffect(() => {
    if (!id) {
      onHide();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  // looking for loading/dispatch
  useEffect(() => {}, [isLoading, dispatch]);

  const deleteIndustry = () => {
    // server request for deleting industry by id
    dispatch(actions.deleteIndustry(id)).then(() => {
      // refresh list after deletion
      dispatch(actions.fetchIndustryList(industryUIProps.queryParams));
      // clear selections list
      industryUIProps.setIds([]);
      // closing delete modal
      onHide();
    });
  };

  return (
    <Modal
      show={show}
      onHide={onHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {isLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Industry Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this industry?</span>
        )}
        {isLoading && <span>Industry is deleting...</span>}
      </Modal.Body>
      <Modal.Footer>
        <div>
          <button
            type="button"
            onClick={onHide}
            className="btn btn-light btn-elevate"
          >
            Cancel
          </button>
          <> </>
          <button
            type="button"
            onClick={deleteIndustry}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
