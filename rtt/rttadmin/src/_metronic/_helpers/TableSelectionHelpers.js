import React from 'react';

const SelectionCheckbox = ({ isSelected }) => (
  <label className="checkbox checkbox-single">
    <input type="checkbox" checked={isSelected} readOnly />
    <span />
  </label>
);

// check official documentations: https://react-bootstrap-table.github.io/react-bootstrap-table2/storybook/index.html?selectedKind=Row%20Selection&selectedStory=Custom%20Selection%20Column%20Header%20Style&full=0&addons=1&stories=1&panelRight=0&addonPanel=storybook%2Factions%2Factions-panel
export const getSelectRow = ({ entities, ids, setIds, isCheckboxClickOnly = false }) => ({
  mode: 'checkbox',
  clickToSelect: true,
  hideSelectAll: false,
  selected: ids,
  onSelect: ({ id: itemId }, isSelect, _, e) => {
    e.preventDefault();

    if (isCheckboxClickOnly && e.target.className === 'selection-cell') {
      return false;
    }

    setIds(isSelect ? [...ids, itemId] : ids.filter(id => id !== itemId))
  },
  onSelectAll: (_, __, e) => {
    e.preventDefault();

    if (isCheckboxClickOnly && e.target.className === 'selection-cell-header') {
      return ids;
    }

    const entitiesIds = entities.map(({ id }) => id);
    const filteredIds = ids.filter(id => !entitiesIds.includes(id));
    const newIds = entitiesIds.every(id => ids.includes(id)) ? filteredIds : [...filteredIds, ...entitiesIds];

    setIds(newIds);
  },
  selectionRenderer: ({ checked: isSelected }) => <SelectionCheckbox isSelected={isSelected} />,
  selectionHeaderRenderer: ({ checked: isSelected }) => <SelectionCheckbox isSelected={isSelected} />,
});
