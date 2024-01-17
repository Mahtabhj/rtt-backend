import React, { useEffect, useMemo, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { newsImpactAssessmentSlice } from '@redux-news/impact-assessment/impactAssessmentSlice';
import { fetchImpactAssessmentList } from '@redux-news/impact-assessment/impactAssessmentActions';

import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
} from '@metronic-partials/controls';
import { ImpactAssessmentTable } from './impact-assessment-table/ImpactAssessmentTable';
import { useImpactAssessmentUIContext } from "./ImpactAssessmentUIContext";

const { actions } = newsImpactAssessmentSlice;

export function ImpactAssessmentCard() {
  const dispatch = useDispatch();
  const impactAssessmentUIContext = useImpactAssessmentUIContext();

  const [_, setDataToSend] = useState({});

  const tab = useSelector(state => state.newsImpactAssessment.tab);

  const queryParams = useMemo(() => impactAssessmentUIContext.queryParams, [impactAssessmentUIContext]);

  useEffect(() => {
    const { pageNumber, pageSize, sortOrder } = queryParams;
    const newDataToSend = { status: tab, pageNumber, pageSize, sort_order: sortOrder || 'desc' };

    setDataToSend(prevState => {
      const isSameDataToSend = prevState.status === newDataToSend.status && prevState.pageNumber === newDataToSend.pageNumber && prevState.pageSize === newDataToSend.pageSize && prevState.sort_order === newDataToSend.sort_order;

      if (isSameDataToSend) {
        return prevState;
      } else {
        dispatch(
          fetchImpactAssessmentList(newDataToSend)
        );

        return newDataToSend
      }
    })
  }, [dispatch, tab, queryParams]);

  const tabChanged = tab => dispatch(actions.setTab(tab));

  return (
    <Card>
      <CardHeader title="Impact Assessment List">
        <CardHeaderToolbar />
      </CardHeader>

      <CardBody>
        <ul className="nav nav-tabs nav-tabs-line" role="tablist">
          <li className="nav-item" onClick={() => tabChanged("to_be_assessed")}>
            <a
                className={`nav-link ${tab === "to_be_assessed" && "active"}`}
                data-toggle="tab"
                role="tab"
                aria-selected={(tab === "to_be_assessed").toString()}
            >
              To be assessed
            </a>
          </li>

          <li className="nav-item" onClick={() => tabChanged("completed")}>
            <a
                className={`nav-link ${tab === "completed" && "active"}`}
                data-toggle="tab"
                role="tab"
                aria-selected={(tab === "completed").toString()}
            >
              Completed
            </a>
          </li>
        </ul>

        <div className="mt-5">
          <ImpactAssessmentTable />
        </div>
      </CardBody>
    </Card>
  );
}
