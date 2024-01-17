import { createSlice } from "@reduxjs/toolkit";

const initialOrganizationState = {
  listLoading: false,
  actionsLoading: false,
  totalCount: 0,
  entities: null,
  organizationForEdit: undefined,
  organizationForSelect: undefined,
  organizationUserForEdit: undefined,
  organizationSubscriptionForEdit: undefined,
  lastError: null,
  users: null,
  subscriptions: null,
  subscriptionTypes: null,
  success: false,
};

export const callTypes = {
  list: "list",
  action: "action",
};

export const organizationSlice = createSlice({
  name: "organization",
  initialState: initialOrganizationState,
  reducers: {
    catchError: (state, action) => {
      state.success = false;
      state.error = `${action.type}: ${action.payload.error}`;
      if (action.payload.callType === callTypes.list) {
        state.listLoading = false;
      } else {
        state.actionsLoading = false;
      }
    },

    startCall: (state, action) => {
      state.error = null;
      state.success = false;
      if (action.payload.callType === callTypes.list) {
        state.listLoading = true;
        state.organizationForSelect =
          initialOrganizationState.organizationForSelect;
      } else {
        state.actionsLoading = true;
        state.organizationForSelect =
          initialOrganizationState.organizationForSelect;
      }
    },

    // getOrganizationById
    organizationFetched: (state, action) => {
      state.actionsLoading = false;
      state.organizationForEdit = action.payload.organizationForEdit;
      state.error = null;
    },

    organizationUserFetched: (state, action) => {
      state.actionsLoading = false;
      state.organizationUserForEdit = action.payload.organizationUserForEdit;
      state.error = null;
    },

    organizationSubscriptionFetched: (state, action) => {
      state.actionsLoading = false;
      state.organizationSubscriptionForEdit =
        action.payload.subscriptionForEdit;
      state.error = null;
    },

    // getOrganizationById
    organizationSelected: (state, action) => {
      state.actionsLoading = false;
      state.organizationForSelect = action.payload.organizationForSelect;
      state.error = null;
    },

    // getOrganizationList
    organizationListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.entities = entities;
      state.totalCount = totalCount;
    },

    // getOrganizationUserList
    organizationUserListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.users = entities;
      state.totalCount = totalCount;
    },

    // getOrganizationUserList
    organizationSubscriptionsListFetched: (state, action) => {
      const { totalCount, entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.subscriptions = entities;
      state.totalCount = totalCount;
    },

    // getOrganizationUserList
    organizationSubscriptionsTypesFetched: (state, action) => {
      const { entities } = action.payload;
      state.listLoading = false;
      state.error = null;
      state.subscriptionTypes = entities;
    },

    // createOrganization
    organizationCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.success = "organization";
      state.entities.push(action.payload.organization);
    },

    // createOrganizationUser
    organizationUserCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.success = "organization-user";
      state.users.push(action.payload.user);
    },

    organizationSubscriptionCreated: (state, action) => {
      state.actionsLoading = false;
      state.error = null;
      state.subscriptions.push(action.payload.subscription);
    },
    // updateOrganization
    organizationUpdated: (state, action) => {
      state.error = null;
      state.success = "organization";
      state.actionsLoading = false;
      state.entities = state.entities.map((entity) => {
        if (entity.id === action.payload.organization.id) {
          return action.payload.organization;
        }
        return entity;
      });
    },

    // updateOrganizationUser
    organizationUserUpdated: (state, action) => {
      state.error = null;
      state.success = "organization-user";
      state.actionsLoading = false;
      state.organizationUserForEdit = action.payload.user;
      state.users = state.users.map((user) => {
        if (user.id === action.payload.user.id) {
          return action.payload.user;
        }
        return user;
      });
    },

    // updateOrganizationSubscription
    organizationSubscriptionUpdated: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.subscriptions = state.subscriptions.map((subscription) => {
        if (subscription.id === action.payload.subscription.id) {
          return action.payload.subscription;
        }
        return subscription;
      });
    },

    // deleteOrganization
    organizationDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.entities = state.entities.filter(
        (el) => el.id !== action.payload.id
      );
    },

    organizationUserDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.users = state.users.filter((user) => user.id !== action.payload.id);
    },

    organizationSubscriptionDeleted: (state, action) => {
      state.error = null;
      state.actionsLoading = false;
      state.subscriptions = state.subscriptions.filter(
        (subscription) => subscription.id !== action.payload.id
      );
    },
  },
});
