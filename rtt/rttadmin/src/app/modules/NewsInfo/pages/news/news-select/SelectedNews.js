import React from "react";
import { Paper, Typography } from "@material-ui/core";

import { SubstancesTable } from "@common";

export const SelectedNews = ({ body, substances }) => (
  <Paper style={{ 'padding': '24px 16px' }}>
    <div className="row">
      <div className="col-12">
        <Typography variant="h6" component="h3">
          News Body
        </Typography>

        <Typography component="p" dangerouslySetInnerHTML={{ __html: body }}/>

        <SubstancesTable substances={substances}/>
      </div>
    </div>
  </Paper>
);
