/* eslint-disable no-restricted-imports */
import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-product/product-category/productCategoryActions";
import { useProductCategoryUIContext } from "../ProductCategoryUIContext";

export function ProductCategoryDeleteDialog({ id, show, onHide }) {
  // ProductCategory UI Context
  const productCategoryUIContext = useProductCategoryUIContext();
  const productCategoryUIProps = useMemo(() => {
    return {
      setIds: productCategoryUIContext.setIds,
      queryParams: productCategoryUIContext.queryParams,
    };
  }, [productCategoryUIContext]);

  // ProductCategory Redux state
  const dispatch = useDispatch();
  const { isLoading } = useSelector(
    (state) => ({ isLoading: state.productCategory.actionsLoading }),
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

  const deleteProductCategory = () => {
    // server request for deleting productCategory by id
    dispatch(actions.deleteProductCategory(id)).then(() => {
      // refresh list after deletion
      dispatch(
        actions.fetchProductCategoryList(productCategoryUIProps.queryParams)
      );
      // clear selections list
      productCategoryUIProps.setIds([]);
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
          Product Category Delete
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!isLoading && (
          <span>Are you sure to permanently delete this product category?</span>
        )}
        {isLoading && <span>Product Category is deleting...</span>}
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
            onClick={deleteProductCategory}
            className="btn btn-delete btn-elevate"
          >
            Delete
          </button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
