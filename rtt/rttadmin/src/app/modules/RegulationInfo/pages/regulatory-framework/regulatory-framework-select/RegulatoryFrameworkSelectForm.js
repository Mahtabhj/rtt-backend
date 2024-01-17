import React from "react";
import { Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(3, 2),
  },
}));

export function RegulatoryFrameworkSelectForm({ regulatoryFramework }) {

  const classes = useStyles();

  return (
    <>
      <Paper className={classes.root}>
        <div className="row">
          <div className="col-6">
            <Typography variant="h6" component="h3">
              Name
            </Typography>
            <Typography component="p">{regulatoryFramework?.name}</Typography>
          </div>

          <div className="col-6">
            <Typography variant="h6" component="h3">
              Status
            </Typography>
            <Typography component="p">
              {regulatoryFramework?.status.name}
            </Typography>
          </div>
        </div>

        <div className="row">
          <div className="col-12">
            <Typography variant="h6" component="h3">
              Description
            </Typography>
            <Typography component="p">
              {regulatoryFramework?.description}
            </Typography>
          </div>
        </div>
      </Paper>
    </>
  );
}
