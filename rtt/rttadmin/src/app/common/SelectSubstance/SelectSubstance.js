import React from "react";
import PropTypes from "prop-types";

import { AddSubstanceManual } from "../RelatedSubstances/components/AddSubstanceManual";

const propTypes = {
  selected: PropTypes.object,
  onChange: PropTypes.func.isRequired,
  children: PropTypes.element,
  isDisabled: PropTypes.bool,
}

const defaultProps = {
  selected: null,
  children: null,
  isDisabled: false,
}

export const SelectSubstance = ({ selected, onChange, children, isDisabled }) => (
  <div className="col-lg-6">
    <label>Substance</label>
    <AddSubstanceManual
      selected={selected ? [selected] : []}
      onChange={onChange}
      isDisabled={isDisabled}
      isValuesShown
      isSingle
    />
    {children}
  </div>
)

SelectSubstance.propTypes = propTypes;
SelectSubstance.defaultProps = defaultProps;
