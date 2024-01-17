import React, { useEffect, useMemo } from "react";
import { Modal } from "react-bootstrap";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import * as actions from "@redux-organization/users/usersActions";
import { UserEditDialogHeader } from "./UserEditDialogHeader";
import { UserEditForm } from "./UserEditForm";
import { useUsersUIContext } from "../UsersUIContext";

export function UserEditDialog({ id, show, onHide }) {
  // Users UI Context
  const usersUIContext = useUsersUIContext();
  const usersUIProps = useMemo(() => {
    return {
      initUser: usersUIContext.initUser,
    };
  }, [usersUIContext]);

  // Users Redux state
  const dispatch = useDispatch();
  const { actionsLoading, userForEdit, organizations, success } = useSelector(
    (state) => ({
      actionsLoading: state.users.actionsLoading,
      userForEdit: state.users.userForEdit,
      organizations: state.users.organizations,
      success: state.users.success,
    }),
    shallowEqual
  );

  useEffect(() => {
    if (success){
      onHide()
    }
  }, [success]);

  useEffect(() => {
    // server call for getting User by id
    dispatch(actions.fetchUser(id));
    dispatch(actions.fetchOrganizationList({ pageSize: 1000 }));
  }, [id, dispatch]);

  // server request for saving user
  const saveUser = (user) => {
    if (!id) {
      // server request for creating user
      delete user.id;
      dispatch(
        actions.createUser({
          ...user,
          username: user.email,
          is_active: JSON.parse(user.is_active),
          is_admin: JSON.parse(user.is_admin),
        })
      );
    } else {
      // server request for updating user
      dispatch(
        actions.updateUser({
          ...user,
          is_active: JSON.parse(user.is_active),
          is_admin: JSON.parse(user.is_admin),
        })
      );
    }
  };

  return (
    <Modal
      size="lg"
      show={show}
      onHide={onHide}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      <UserEditDialogHeader id={id} />
      <UserEditForm
        saveUser={saveUser}
        actionsLoading={actionsLoading}
        user={
          userForEdit || {
            ...usersUIProps.initUser,
            organization:
              organizations && organizations.length > 0
                ? organizations[0].id
                : undefined,
          }
        }
        onHide={onHide}
        organizations={organizations || []}
      />
    </Modal>
  );
}
