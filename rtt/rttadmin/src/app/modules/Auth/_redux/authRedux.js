import { persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";
import { put, takeLatest } from "redux-saga/effects";
import { getUserByToken, getUserPermissions } from "./authCrud";

export const actionTypes = {
  Login: "[Login] Action",
  Logout: "[Logout] Action",
  Register: "[Register] Action",
  UserRequested: "[Request User] Action",
  UserLoaded: "[Load User] Auth API",
  PermissionsRequested: "[Request Permissions] Auth API",
  PermissionsLoaded: "[Load Permissions] Auth API",
};

const initialAuthState = {
  user: undefined,
  authToken: undefined,
  permissions: [],
  isPermissionsLoaded: false,
};

export const reducer = persistReducer(
  { storage, key: "rtt-admin-auth", whitelist: ["user", "authToken"] },
  (state = initialAuthState, action) => {
    switch (action.type) {

      case actionTypes.Login: {
        const { authToken } = action.payload;
        return { authToken, user: undefined };
      }

      case actionTypes.Logout: {
        return initialAuthState;
      }

      case actionTypes.UserLoaded: {
        const { user } = action.payload;
        return { ...state, user };
      }

      case actionTypes.PermissionsRequested: {
        return { ...state, isPermissionsLoaded: false }
      }

      case actionTypes.PermissionsLoaded: {
        const { permissions } = action.payload;
        // const permissions = [
        // 'organization', 'user',
        // 'news', 'newsassessmentworkflow', 'source',
        // 'regulatoryframework', 'regulation', 'issuingbody', 'answer',
        // 'substance', 'substancefamily',
        // 'regulationsubstancelimit', 'exemption',
        // 'industry', 'productcategory', 'materialcategory',
        // 'document' ]; // uncomment to test permissions
        return { ...state, permissions, isPermissionsLoaded: true };
      }

      default:
        return state;
    }
  }
);

export const actions = {
  login: authToken => ({ type: actionTypes.Login, payload: { authToken } }),
  register: authToken => ({ type: actionTypes.Register, payload: { authToken }}),
  logout: () => ({ type: actionTypes.Logout }),
  requestUser: user => ({ type: actionTypes.UserRequested, payload: { user } }),
  fulfillUser: user => ({ type: actionTypes.UserLoaded, payload: { user } }),
  requestPermissions: () => ({ type: actionTypes.PermissionsRequested }),
  updatePermissions: permissions => ({ type: actionTypes.PermissionsLoaded, payload: { permissions } }),
};

export function* saga() {
  yield takeLatest(actionTypes.Login, function* loginSaga() {
    yield put(actions.requestUser());
  });

  yield takeLatest(actionTypes.Register, function* registerSaga() {
    yield put(actions.requestUser());
  });

  yield takeLatest(actionTypes.UserRequested, function* userRequested() {
    const { data: user } = yield getUserByToken();
    yield put(actions.fulfillUser(user));
  });

  yield takeLatest(actionTypes.PermissionsRequested, function* permissionsSaga() {
    const { data: permissions } = yield getUserPermissions();
    yield put(actions.updatePermissions(permissions));
  });
}
