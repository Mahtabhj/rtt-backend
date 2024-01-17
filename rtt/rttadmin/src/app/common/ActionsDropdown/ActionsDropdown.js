import React from 'react';
import { Dropdown, DropdownButton } from 'react-bootstrap';
import PropTypes from 'prop-types';
import cx from 'classnames';

import './ActionsDropdown.scss';

const propTypes = {
  title: PropTypes.string.isRequired,
  buttons: PropTypes.arrayOf(PropTypes.shape({
    actionName: PropTypes.string.isRequired,
    actionCallback: PropTypes.func.isRequired,
    isDanger: PropTypes.bool,
  })).isRequired,
};

export const ActionsDropdown = ({ title, buttons}) => (
  <DropdownButton id="actions-dropdown" title={title}>
    <Dropdown className="actions-dropdown">
      {buttons.map(({ actionName, actionCallback, isDanger = false }) => (
        <Dropdown.Item
          bsPrefix={cx("actions-dropdown__button", isDanger ? 'btn-outline-danger' : 'btn-outline-primary' )}
          onClick={actionCallback}
          key={actionName}
        >
          {actionName}
        </Dropdown.Item>
      ))}
    </Dropdown>
  </DropdownButton>
);

ActionsDropdown.propTypes = propTypes;
