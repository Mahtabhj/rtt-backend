import React, { useCallback, useMemo } from "react";
import { useHistory } from "react-router-dom";
import PropTypes from "prop-types";

import { headerFormatter } from "@metronic-helpers";

import { getTextFilter } from "@common/Filters";
import { UiKitTable } from "@common/UIKit";

import { FAMILY_TAB, SUBSTANCE_MAIN_PATH } from "../../../SubstanceRoutes";

import * as columnFormatters from "./column-formatters";

export const headerStyle = { fontSize: '10px' };

const propTypes = {
  list: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    chemycal_id: PropTypes.string,
    name: PropTypes.string.isRequired,
    number_of_substances: PropTypes.number.isRequired,
  })).isRequired,
  customOptions: PropTypes.object.isRequired,
  openDeleteFamilyDialog: PropTypes.func.isRequired,
  onTableChangeCallback: PropTypes.func.isRequired,
};

export const FamilyTable = ({ list, customOptions, openDeleteFamilyDialog, onTableChangeCallback }) => {
  const history = useHistory();

  const openEditFamilyPage = useCallback(familyId =>
    history.push(`${SUBSTANCE_MAIN_PATH}/${FAMILY_TAB}/${familyId}/edit`)
    , [history]);

  const columns = useMemo(
    () => [
      {
        dataField: 'id',
        text: 'ID',
        headerFormatter,
        headerStyle,
      },
      {
        dataField: 'chemycal_id',
        text: 'Chemycal Id',
        headerFormatter,
        headerStyle,
        ...getTextFilter(),
      },
      {
        dataField: 'family_name',
        text: 'Name',
        formatter: (_, { name }) => name,
        headerFormatter,
        headerStyle,
        ...getTextFilter(),
      },
      {
        dataField: 'number_of_substances',
        text: 'Substances #',
        headerFormatter,
        headerStyle,
      },
      {
        dataField: 'action',
        text: 'Actions',
        formatter: columnFormatters.ActionsColumnFormatter,
        formatExtraData: {
          openEditFamilyPage,
          openDeleteFamilyDialog,
        },
        classes: 'text-right pr-0',
        headerClasses: 'text-right pr-3',
        style: { minWidth: '100px' },
      }
    ],
    [openEditFamilyPage],
  );

  return (
    <UiKitTable
      list={list}
      columns={columns}
      customOptions={customOptions}
      onTableChangeCallback={onTableChangeCallback}
    />
  );
};

FamilyTable.propTypes = propTypes;
