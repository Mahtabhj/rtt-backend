/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-product/material-category/materialCategoryActions";
import { useMaterialCategoryUIContext } from "../MaterialCategoryUIContext";

export function MaterialCategoryDeleteDialog({ id, show, onHide }) {
  // MaterialCategory UI Context
  const materialCategoryUIContext = useMaterialCategoryUIContext();
  const materialCategoryUIProps = useMemo(() => {
    return {
      setIds: materialCategoryUIContext.setIds,
      queryParams: materialCategoryUIContext.queryParams,
    };
  }, [materialCategoryUIContext]);

  // MaterialCategory Redux state
  const dispatch = useDispatch();
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.materialCategory.actionsLoading }),
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

  const deleteMaterialCategory = () => {
    // server request for deleting materialCategory by id
    dispatch(actions.deleteMaterialCategory(id)).then(() => {
      // refresh list after deletion
      dispatch(
        actions.fetchMaterialCategoryList(materialCategoryUIProps.queryParams)
      );
      // clear selections list
      materialCategoryUIProps.setIds([]);
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
          Material Category Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>
            Are you sure to permanently delete this material category?
          </span>
        )}
        {isLoading && <span>Material Category is deleting...</span>}
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
            onClick={deleteMaterialCategory}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
