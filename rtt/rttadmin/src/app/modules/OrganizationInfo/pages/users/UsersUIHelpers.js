export const UserStatusCssClasses = ["success", "danger"];
export const OrganizationStatusTitles = ["Active", "Inactive"];
export const UserTypeCssClasses = ["success", "primary", ""];
export const UserTypeTitles = ["Business", "Individual", ""];
export const defaultSorted = [{ dataField: "id", order: "asc" }];

export const UserTitles = ["User", "Org Admin"];

export const sizePerPageList = [
  { text: "100", value: 100 },
  { text: "200", value: 200 },
  { text: "300", value: 300 },
];
export const initialFilter = {
  filter: {
    lastName: "",
    firstName: "",
    email: "",
    ipAddress: "",
  },
  sortOrder: "asc", // asc||desc
  sortField: "id",
  pageNumber: 1,
  pageSize: 100,
};
