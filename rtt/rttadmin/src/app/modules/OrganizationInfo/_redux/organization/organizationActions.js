import * as organizationApiService from "./organizationApiService";
import { organizationSlice, callTypes } from "./organizationSlice";

const { actions } = organizationSlice;

export const fetchOrganizationList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return organizationApiService
    .getOrganizationList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.organizationListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find organization";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchOrganization = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.organizationFetched({ organizationForEdit: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .getOrganizationById(id)
    .then((response) => {
      const organization = response.data;
      dispatch(
        actions.organizationFetched({ organizationForEdit: organization })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const selectOrganization = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.organizationSelected({ organizationForSelect: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .getOrganizationById(id)
    .then((response) => {
      const organization = response.data;
      dispatch(
        actions.organizationSelected({ organizationForSelect: organization })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteOrganization = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .deleteOrganization(id)
    .then((response) => {
      dispatch(actions.organizationDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createOrganization = (organizationForCreation) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .createOrganization(organizationForCreation)
    .then((response) => {
      const organization = response.data;
      dispatch(actions.organizationCreated({ organization }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateOrganization = (organization) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .updateOrganization(organization)
    .then(() => {
      dispatch(actions.organizationUpdated({ organization }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const chnageUserPassword = (data) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .changePassword(data)
    .then((res) => {
      console.info(res);
    })
    .catch((error) => {
      error.clientMessage = "Can't change password";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchOrganizationUserList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return organizationApiService
    .getOrganizationUserList(queryParams)
    .then((response) => {
      const totalCount = 0;
      const entities = response.data.results;
      dispatch(actions.organizationUserListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find organization";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchOrganizationSelectedUser = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.organizationUserFetched({ organizationUserForEdit: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .getOrganizationUserById(id)
    .then((response) => {
      const user = response.data;
      dispatch(
        actions.organizationUserFetched({ organizationUserForEdit: user })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createOrganizationUser = (user) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .createOrganizationUser(user)
    .then((response) => {
      const user = response.data;
      dispatch(actions.organizationUserCreated({ user }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateOrganizationUser = (user) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .updateOrganizationUser(user)
    .then(() => {
      user.is_admin === "true"
        ? (user.is_admin = true)
        : (user.is_admin = false);
      dispatch(actions.organizationUserUpdated({ user }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteOrganizationUser = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .deleteOrganizationUser(id)
    .then((response) => {
      dispatch(actions.organizationUserDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createOrganizationSubscription = (subscription) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .createOrganizationSubscription(subscription)
    .then((response) => {
      const subscription = response.data;
      dispatch(actions.organizationSubscriptionCreated({ subscription }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create subscription";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteOrganizationSubscription = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .deleteOrganizationSubscription(id)
    .then((response) => {
      dispatch(actions.organizationSubscriptionDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchOrganizationSelectedSubscription = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.organizationSubscriptionFetched({
        subscriptionForEdit: undefined,
      })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .getOrganizationSubscriptionById(id)
    .then((response) => {
      const subscription = response.data;
      dispatch(
        actions.organizationSubscriptionFetched({
          subscriptionForEdit: subscription,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchOrganizationSubscriptionTypes = () => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return organizationApiService
    .getOrganizationSubscriptionTypes()
    .then((response) => {
      const entities = response.data.results;
      dispatch(actions.organizationSubscriptionsTypesFetched({ entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find organization";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchOrganizationSubscriptionList = (queryParams) => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return organizationApiService
    .getOrganizationSubscriptionList(queryParams)
    .then((response) => {
      const totalCount = 0;
      const entities = response.data;
      dispatch(
        actions.organizationSubscriptionsListFetched({ totalCount, entities })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find organization";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const updateOrganizationSubscription = (subscription) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return organizationApiService
    .updateOrganizationSubscription(subscription)
    .then(() => {
      dispatch(actions.organizationSubscriptionUpdated({ subscription }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update organization";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};
