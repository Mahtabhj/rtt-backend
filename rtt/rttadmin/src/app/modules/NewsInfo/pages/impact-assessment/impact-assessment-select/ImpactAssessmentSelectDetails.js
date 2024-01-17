import React from "react";

import { Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import {
  formatDateDDMMYYY,
  formatCategoriesNames,
  formatRegionsNames,
  formatRegulationsNames,
  formatFrameworksNames,
  formatProductCategoriesNames,
  formatMaterialCategoriesNames
} from "@metronic-helpers";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(3, 2),
  },
}));

export function ImpactAssessmentSelectDetails({ impactAssessment }) {
  const classes = useStyles();

  const {
    pub_date,
    news_categories = [],
    source,
    regions = [],
    regulations = [],
    regulatory_frameworks = [],
    product_categories = [],
    material_categories = [],
  } = impactAssessment || {};

  const renderImpactAssessmentDetailsItem = (title, subtitle) => (
    <div className="col row flex-row align-items-baseline">
      <Typography variant="h6" component="h3" className="mr-1">
        {title}:
      </Typography>
      <Typography component="p">{subtitle}</Typography>
    </div>)

  return (
    <>
      <Paper className={classes.root}>
        <div className="col row">
          {renderImpactAssessmentDetailsItem('Publish date', formatDateDDMMYYY(pub_date))}

          {renderImpactAssessmentDetailsItem('Source', source?.name)}

          {renderImpactAssessmentDetailsItem('Categories', formatCategoriesNames(news_categories))}
        </div>

        <div className="col row">
          {renderImpactAssessmentDetailsItem('Regions', formatRegionsNames(regions))}

          {renderImpactAssessmentDetailsItem('Regulations', formatRegulationsNames(regulations))}

          {renderImpactAssessmentDetailsItem('Frameworks', formatFrameworksNames(regulatory_frameworks))}
        </div>

        <div className="col row">
          {renderImpactAssessmentDetailsItem('Product category', formatProductCategoriesNames(product_categories))}

          {renderImpactAssessmentDetailsItem('Material category', formatMaterialCategoriesNames(material_categories))}

          <div className="col row" />
        </div>
      </Paper>
    </>
  );
}
