import React, { useEffect, useState } from 'react';
import CheckboxTree from 'react-checkbox-tree';
import PropTypes from 'prop-types';

import { Search } from '../Search/Search';

import 'react-checkbox-tree/lib/react-checkbox-tree.css';

const propTypes = {
  title: PropTypes.string.isRequired,
  categoriesTree: PropTypes.arrayOf(PropTypes.object).isRequired,
  checked: PropTypes.arrayOf(PropTypes.number).isRequired,
  setChecked: PropTypes.func.isRequired,
  expandMap: PropTypes.object.isRequired,
  isForcedUpdate: PropTypes.bool.isRequired,
  disabled: PropTypes.bool.isRequired,
}

export const SelectCategories = ({
  title,
  categoriesTree,
  checked,
  setChecked,
  expandMap,
  isForcedUpdate,
  disabled,
}) => {
  const [search, setSearch] = useState('');
  const [isExpandNecessary, setExpandNecessary] = useState(true);
  const [expanded, setExpanded] = useState([]);
  const [filteredNodes, setFilteredNotes] = useState(categoriesTree);

  useEffect(() => {
      if (!search) {
        // reset nodes back to unfiltered state
        setFilteredNotes(categoriesTree);
        setExpandNecessary(true);
      } else {
        let forExpand = [];

        const filterNodes = (filtered, node) => {
          const children = (node.children || []).reduce(filterNodes, []);

          if (
            // the label matches the search
            node.label.toLocaleLowerCase().indexOf(search.toLocaleLowerCase()) > -1 ||
            // or a children has a matching node
            children.length
          ) {
            filtered.push({ ...node, children });

            if (!children.length) {
              forExpand = [...forExpand, ...expandMap[node.value]]
            }
          }

          return filtered;
        }

        const filteredCategoriesTree = categoriesTree.map(industry => ({
          ...industry,
          children: industry.children.reduce(filterNodes, [])
        }));

        setFilteredNotes(filteredCategoriesTree);
        setExpanded(Array.from(new Set(forExpand)));
      }
    }
  , [categoriesTree, search]);

  useEffect(() => {
    const isShouldUpdate = !!(expandMap && (
      isExpandNecessary || isForcedUpdate
    ));

    if (isShouldUpdate) {
      let forExpand = [];
      checked.forEach(checked => {
        forExpand = [...forExpand, ...expandMap[checked]];
      });

      setExpanded(Array.from(new Set(forExpand)));

      setExpandNecessary(false);
    }
  }, [checked, isForcedUpdate, expandMap, isExpandNecessary]);

  const handleSelectCategories = newChecked => setChecked(newChecked.map(item => +item));
  const handleExpandCategories = newExpanded => setExpanded(newExpanded.map(item => +item));

  return (
    <div className="col-lg-6 mb-5">
      <div className="mb-2" style={{ width: 'fit-content' }}>
        <p className="h3 text-primary">{title}</p>
        <Search initialValue={search} handleUpdateSearch={setSearch} />
      </div>
      <CheckboxTree
        iconsClass="fa5"
        nodes={filteredNodes}
        checked={checked}
        onCheck={handleSelectCategories}
        expanded={expanded}
        onExpand={handleExpandCategories}
        disabled={disabled}
        noCascade
      />
    </div>
  );
}

SelectCategories.propTypes = propTypes;
