import { Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import React from "react";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(3, 2),
  },
}));

export function IssuingBodySelectForm({ issuingbody }) {
  const classes = useStyles();

  return (
    <>
      <Paper className={classes.root}>
        <div className="row">
          <div className="col-6">
            <Typography variant="h6" component="h3">
              Name
            </Typography>
            <Typography component="p">{issuingbody?.name}</Typography>
          </div>

          <div className="col-6">
            <Typography variant="h6" component="h3">
              Region
            </Typography>
            <Typography component="p">{issuingbody?.region}</Typography>
          </div>
        </div>

        <div className="row">
          <div className="col-12">
            <Typography variant="h6" component="h3">
              Description
            </Typography>
            <Typography component="p">{issuingbody?.description}</Typography>
          </div>
        </div>
      </Paper>
    </>
  );
}
