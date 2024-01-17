export const TAB = {
  NEW: 'new',
  SELECTED: 'selected',
  ONLINE: 'online',
  DISCHARGED: 'discharged',
  REVIEW: 'review',
};

export const tabFilterOption = {
  [TAB.NEW]: { status: 'n' },
  [TAB.SELECTED]: { status: 's', active: 'false' },
  [TAB.ONLINE]: { status: 's', active: 'true' },
  [TAB.DISCHARGED]: { status: 'd' },
  [TAB.REVIEW]: { review_yellow: 'true', review_green: 'false' },
};
