import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useHistory, useParams } from "react-router-dom";
import Typography from "@material-ui/core/Typography";

import * as actions from "@redux-news/impact-assessment/impactAssessmentActions";
import * as newsActions from "@redux-news/news/newsActions";

import {
  Card,
  CardBody,
  CardHeader,
  CardHeaderToolbar,
  ModalProgressBar
} from "@metronic-partials/controls";

import { getBoolString, CustomLink } from "@common";

import { ImpactAssessmentSelectBody } from "./ImpactAssessmentSelectBody";
import { ImpactAssessmentSelectDetails } from "./ImpactAssessmentSelectDetails";
import { NewsRelevanceTable } from "./news-relevance-list/NewsRelevanceTable";

export function ImpactAssessmentSelect() {
  const history = useHistory();
  const { id } = useParams();
  const dispatch = useDispatch();

  const [tab, setTab] = useState('impact-assessment');

  const { actionsLoading, impactAssessmentForSelect, newsForSelect } = useSelector(
    (state) => ({
      actionsLoading: state.news.actionsLoading,
      impactAssessmentForSelect: state.newsImpactAssessment.impactAssessmentForSelect,
      newsForSelect: state.news.newsForSelect,
    }),
  );

  useEffect(() => {
    dispatch(actions.selectImpactAssessment(id));
  }, [dispatch, id]);

  useEffect(() => {
    dispatch(newsActions.selectNews(impactAssessmentForSelect?.news?.id));
  }, [dispatch, impactAssessmentForSelect]);

  const backToImpactAssessmentList = () => history.push(`/backend/news-info/impactAssessment`);

  return (
    <>
      <Card>
        {actionsLoading && <ModalProgressBar/>}
        <CardHeader title="Access news:">
          <Typography variant="h6" component="h3" className="flex-row align-self-center mr-auto font-weight-normal">
            {!!newsForSelect?.id && (
              <CustomLink id={newsForSelect?.id} title={newsForSelect?.title} type='news' />
            )}
          </Typography>
          <CardHeaderToolbar>
            <button
              type="button"
              onClick={backToImpactAssessmentList}
              className="btn btn-light"
            >
              <i className="fa fa-arrow-left"/>
              Back
            </button>
          </CardHeaderToolbar>
        </CardHeader>

        <CardBody>
          <ImpactAssessmentSelectBody news={newsForSelect}/>
        </CardBody>

        <ImpactAssessmentSelectDetails impactAssessment={newsForSelect} />
      </Card>

      <Card>
        <CardBody>
          <ul className="nav nav-tabs nav-tabs-line " role="tablist">
            <li
              className="nav-item"
              onClick={() => setTab("impact-assessment")}
            >
              <a
                className={`nav-link ${tab === "impact-assessment" && "active"}`}
                data-toggle="tab"
                role="tab"
                aria-selected={getBoolString(tab === "impact-assessment")}
                href="#/"
              >
                Impact Assessment
              </a>
            </li>
          </ul>
          <div className="mt-5">
            <NewsRelevanceTable
              showNewRelevanceButton={impactAssessmentForSelect?.status === 'to_be_assessed'}
            />
          </div>
        </CardBody>
      </Card>
    </>
  );
}
