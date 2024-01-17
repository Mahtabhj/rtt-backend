import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

import { getRelevantOrganizations as getNewsRelevantOrganizations } from '@redux/commonApiService';
import { getRegulationRelevantOrganizations } from '@redux-regulation/regulation/regulationApiService';
import { getRegulatoryFrameworkRelevantOrganizations } from '@redux-regulation/regulatory-framework/regulatoryFrameworkApiService';

import { NEWS, REGULATION, REGULATORY_FRAMEWORK } from '../constants';
import content from './content';

// please use custom hook to manipulate values:
//
// const [relevantOrganizationsValues, updateRelevantOrganizationsValues] = useOrganizationsValues(
//   relevantOrganizationsValuesInitialState, // initialValuesForRelevantOrganization by default
// );
//
// to update values:
// updateRelevantOrganizationsValues({
//   ...one or several keys, same as in relevantOrganizationsValuesInitialState: related ids array
// });
//
// <VisibleToOrganization type={type} valuesForRelevantOrganizations={relevantOrganizationsValues} />

const getRelevantOrganizations = {
  [NEWS]: getNewsRelevantOrganizations,
  [REGULATION]: getRegulationRelevantOrganizations,
  [REGULATORY_FRAMEWORK]: getRegulatoryFrameworkRelevantOrganizations,
};

const propTypes = {
  valuesForRelevantOrganizations: PropTypes.shape({
    product_categories: PropTypes.arrayOf(PropTypes.number).isRequired,
    material_categories: PropTypes.arrayOf(PropTypes.number).isRequired,
    topics: PropTypes.arrayOf(PropTypes.number),
    regulations: PropTypes.arrayOf(PropTypes.number),
    frameworks: PropTypes.arrayOf(PropTypes.number),
  }).isRequired,
  type: PropTypes.oneOf([NEWS, REGULATION, REGULATORY_FRAMEWORK]).isRequired,
};

export function VisibleToOrganization({ type, valuesForRelevantOrganizations }) {
  const [isLoading, setLoading] = useState(false);
  const [relevantOrganizations, setRelevantOrganizations] = useState([]);

  useEffect(() => {
    let isSubscribed = true;

    const isAnyValue = Object.values(valuesForRelevantOrganizations).some(value => !!value.length);

    if (isAnyValue) {
      setLoading(true);

      getRelevantOrganizations[type](valuesForRelevantOrganizations)
        .then(response => {
          if (isSubscribed) {
            setRelevantOrganizations(response.data);
            setLoading(false);
          }
        })
        .catch(error => console.error(error));
    } else {
      setRelevantOrganizations([]);
    }

    return () => {
      isSubscribed = false;
    };
  }, [type, valuesForRelevantOrganizations]);

  return (
    <div className="relevant-organizations">
      <span className="h3 text-primary">{content.title[type]} visible to organizations:</span>

      {isLoading ? (
        <span className="ml-3 spinner spinner-primary" />
      ) : (
        <span>{relevantOrganizations.length ? relevantOrganizations.map(org => org.name).join(', ') : 'none'}</span>
      )}
    </div>
  );
}

VisibleToOrganization.propTypes = propTypes;
