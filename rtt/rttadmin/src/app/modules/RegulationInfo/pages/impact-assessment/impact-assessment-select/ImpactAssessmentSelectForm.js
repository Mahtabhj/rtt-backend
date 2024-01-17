import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { Input } from "@metronic-partials/controls";
import Select from "react-select";
import * as impactAssessmentApiService from "@redux-regulation/impact-assessment/impactAssessmentApiService";
import { Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import * as columnFormatters from "../impact-assessment-table/column-formatters/StatusColumnFormatter";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(3, 2),
  },
}));

export function ImpactAssessmentSelectForm({ impactAssessment }) {
  const classes = useStyles();

  return (
    <>
      <Paper className={classes.root}>
        <div className="row">
          <div className="col-6">
            <Typography variant="h6" component="h3">
              Name
            </Typography>
            <Typography component="p">{impactAssessment?.name}</Typography>
          </div>

          <div className="col-6">
            <Typography variant="h6" component="h3">
              Region
            </Typography>
            <Typography component="p">{impactAssessment?.region}</Typography>
          </div>
        </div>

        <div className="row">
          <div className="col-12">
            <Typography variant="h6" component="h3">
              Description
            </Typography>
            <Typography component="p">
              {impactAssessment?.description}
            </Typography>
          </div>
        </div>
      </Paper>
    </>
  );
}
