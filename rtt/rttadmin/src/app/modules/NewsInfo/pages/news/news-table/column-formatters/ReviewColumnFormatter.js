import React from 'react';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

import { CheckboxBlank } from "@common";

export const ReviewColumnFormatter = (
  cellContent,
  row,
  rowIndex,
  { handleReviewYellow, handleReviewGreen }
) => {
  const handleOnClickYellow = () => handleReviewYellow(row.id);
  const handleOnClickGreen = () => handleReviewGreen(row.id, !row.review_green);

  const renderReviewYellow = () => (
    <CheckboxBlank
      isSelected={!!row.review_yellow}
      onClick={handleOnClickYellow}
      type="yellow"
    />
  )

  return (
    <div className="d-flex flex-column align-items-center">
      {row.review_comment ? (
        <OverlayTrigger overlay={<Tooltip>{row.review_comment}</Tooltip>}>
          <div>
            {renderReviewYellow()}
          </div>
        </OverlayTrigger>
      ) : (
        renderReviewYellow()
      )}

      <CheckboxBlank
        isSelected={!!row.review_green}
        onClick={handleOnClickGreen}
        type="green"
      />
    </div>
  )
};
