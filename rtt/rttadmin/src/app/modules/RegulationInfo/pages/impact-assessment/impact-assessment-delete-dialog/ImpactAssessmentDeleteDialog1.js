// /* eslint-disable no-restricted-imports */
// import React, { useEffect, useMemo } from "react";
// import { Modal } from "react-bootstrap";
// import { shallowEqual, useDispatch, useSelector } from "react-redux";
// import * as actions from "@redux-regulation/impact-assessment/impactAssessmentActions";
// import { useImpactAssessmentUIContext } from "../ImpactAssessmentUIContext";

// export function ImpactAssessmentDeleteDialog({ id, show, onHide }) {
//   // ImpactAssessment UI Context
//   const impactAssessmentUIContext = useImpactAssessmentUIContext();
//   const impactAssessmentUIProps = useMemo(() => {
//     return {
//       setIds: impactAssessmentUIContext.setIds,
//       queryParams: impactAssessmentUIContext.queryParams,
//     };
//   }, [impactAssessmentUIContext]);

//   // ImpactAssessment Redux state
//   const dispatch = useDispatch();
//   const { isLoading } = useSelector(
//     (state) => ({ isLoading: state.impactAssessment.actionsLoading }),
//     shallowEqual
//   );

//   // if !id we should close modal
//   useEffect(() => {
//     if (!id) {
//       onHide();
//     }
//     // eslint-disable-next-line react-hooks/exhaustive-deps
//   }, [id]);

//   // looking for loading/dispatch
//   useEffect(() => {}, [isLoading, dispatch]);

//   const deleteImpactAssessment = () => {
//     // server request for deleting impactAssessment by id
//     dispatch(actions.deleteImpactAssessment(id)).then(() => {
//       // refresh list after deletion
//       dispatch(actions.fetchImpactAssessmentList(impactAssessmentUIProps.queryParams));
//       // clear selections list
//       impactAssessmentUIProps.setIds([]);
//       // closing delete modal
//       onHide();
//     });
//   };

//   return (
//     <Modal
//       show={show}
//       onHide={onHide}
//       aria-labelledby="example-modal-sizes-title-lg"
//     >
//       {isLoading && <ModalProgressBar variant="query" />}
//       <Modal.Header closeButton>
//         <Modal.Title id="example-modal-sizes-title-lg">
//           ImpactAssessment Delete
//         </Modal.Title>
//       </Modal.Header>
//       <Modal.Body>
//         {!isLoading && (
//           <span>Are you sure to permanently delete this impactAssessment?</span>
//         )}
//         {isLoading && <span>ImpactAssessment is deleting...</span>}
//       </Modal.Body>
//       <Modal.Footer>
//         <div>
//           <button
//             type="button"
//             onClick={onHide}
//             className="btn btn-light btn-elevate"
//           >
//             Cancel
//           </button>
//           <> </>
//           <button
//             type="button"
//             onClick={deleteImpactAssessment}
//             className="btn btn-delete btn-elevate"
//           >
//             Delete
//           </button>
//         </div>
//       </Modal.Footer>
//     </Modal>
//   );
// }
