import { Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import React from "react";
const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(3, 2),
  },
}));

export function DocumentSelectForm({ document }) {
  const classes = useStyles();

  return (
    <>
      <Paper className={classes.root}>
        <div className="row">
          <div className="col-6">
            <Typography variant="h6" component="h3">
              Document Name
            </Typography>
            <Typography component="p">{document?.title}</Typography>
          </div>

          <div className="col-6">
            <Typography variant="h6" component="h3">
              Document Type
            </Typography>
            <Typography component="p">{document?.type}</Typography>
          </div>
        </div>

        <div className="row">
          <div className="col-12">
            <Typography variant="h6" component="h3">
              Document Description
            </Typography>
            <Typography component="p">{document?.description}</Typography>
          </div>
        </div>
      </Paper>
    </>
  );
}
