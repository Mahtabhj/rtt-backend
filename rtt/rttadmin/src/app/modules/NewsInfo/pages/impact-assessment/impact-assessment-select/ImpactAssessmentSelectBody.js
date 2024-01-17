import React from "react";

import { Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

import { SubstancesTable } from "@common";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(3, 2),
  },
}));

export function ImpactAssessmentSelectBody({ news }) {
  const classes = useStyles();

  return (
    <>
      <Paper className={classes.root}>
        <div className="row">
          <div className="col-12">
            <Typography variant="h6" component="h3">
              News Body
            </Typography>

            <Typography component="p" dangerouslySetInnerHTML={{ __html: news?.body }} />

            <div className="mt-5">
              <SubstancesTable substances={news?.substances || []} />
            </div>
          </div>
        </div>
      </Paper>
    </>
  );
}
