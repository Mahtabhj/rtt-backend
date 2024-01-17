import React, { useEffect, useState } from "react";

import { Modal } from "react-bootstrap";
import { ModalProgressBar } from "@metronic-partials/controls";
import * as actions from "@redux-organization/organization/organizationActions";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { v4 as uuidv4 } from "uuid";
import dayjs from "dayjs";

import { SubscriptionForm } from "./SubscriptionForm";

export function SubscriptionAddEditModal({
  showSubscriptionAddModal,
  setShowSubscriptionAddModal,
  selectedSubscriptionId,
  organizationId,
}) {
  const dispatch = useDispatch();

  const {
    actionsLoading,
    organizationSubscriptionForEdit,
    organizationSubscriptionTypes,
  } = useSelector(
    (state) => ({
      actionsLoading: state.organization.actionsLoading,
      organizationSubscriptionForEdit:
        state.organization.organizationSubscriptionForEdit,
      organizationSubscriptionTypes: state.organization.subscriptionTypes,
    }),
    shallowEqual
  );

  const [initSubscription, setInitSubscription] = useState({
    start_date: dayjs(),
    end_date: dayjs(),
    paid: true,
    amount: 0,
    max_user: 1,
    type: null,
    organization: 0,
  });

  useEffect(() => {
    if (organizationSubscriptionForEdit) {
      setInitSubscription(organizationSubscriptionForEdit);
    } else {
      organizationSubscriptionTypes &&
        organizationSubscriptionTypes.length > 0 &&
        setInitSubscription((initSubscription) => ({
          ...initSubscription,
          type: organizationSubscriptionTypes[0].id,
        }));
    }
  }, [organizationSubscriptionTypes, organizationSubscriptionForEdit]);

  useEffect(() => {
    dispatch(
      actions.fetchOrganizationSelectedSubscription(selectedSubscriptionId)
    );
    dispatch(actions.fetchOrganizationSubscriptionTypes());
  }, [selectedSubscriptionId, dispatch]);

  const saveOrganizationSubscription = (values) => {
    if (!selectedSubscriptionId) {
      dispatch(
        actions.createOrganizationSubscription({
          ...values,
          start_date: dayjs(values.start_date).toISOString(),
          end_date: dayjs(values.end_date).toISOString(),
          invoice_uid: uuidv4(),
          organization: organizationId,
        })
      ).then(() => setShowSubscriptionAddModal(false));
    } else {
      dispatch(actions.updateOrganizationSubscription({
        ...values,
        start_date: dayjs(values.start_date).toISOString(),
        end_date: dayjs(values.end_date).toISOString()
      })).then(() =>
        setShowSubscriptionAddModal(false)
      );
    }
  };

  return (
    <Modal
      size="lg"
      show={showSubscriptionAddModal}
      onHide={() => setShowSubscriptionAddModal(false)}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      {actionsLoading && <ModalProgressBar variant="query" />}
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          Add Organization Subscription
        </Modal.Title>
      </Modal.Header>

      <SubscriptionForm
        setShowSubscriptionAddModal={setShowSubscriptionAddModal}
        saveOrganizationSubscription={saveOrganizationSubscription}
        subscription={organizationSubscriptionForEdit || initSubscription}
        organizationSubscriptionTypes={organizationSubscriptionTypes || []}
      />
    </Modal>
  );
}
