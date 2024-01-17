import React from "react";
import { Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(3, 2),
  },
}));

export function SourceSelectForm({ source }) {
  const classes = useStyles();

  return (
    <>
      <Paper className={classes.root}>
        <div className="row">
          <div className="col-6">
            <Typography variant="h6" component="h3">
              Source Name
            </Typography>
            <Typography component="p">{source?.name}</Typography>
          </div>

          <div className="col-6">
            <Typography variant="h6" component="h3">
              Source Link
            </Typography>
            <Typography component="p">{source?.link}</Typography>
          </div>
        </div>

        <div className="row">
          <div className="col-12">
            <Typography variant="h6" component="h3">
              Source Description
            </Typography>
            <Typography component="p">{source?.description}</Typography>
          </div>
        </div>
      </Paper>
    </>
  );
}
