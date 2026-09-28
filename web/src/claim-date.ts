/** Display only recorded temporal meaning; numeric years remain selection indices. */
export type ClaimDateFields = {
  date_text_original?: string | null;
  temporal_precision?: string | null;
  temporal_certainty?: string | null;
};

export function claimDateDetail(claim: ClaimDateFields): {
  sourceDate: string | null;
  qualifier: string | null;
  selectionNote: string | null;
} {
  const precision = claim.temporal_precision;
  const certainty = claim.temporal_certainty;
  const label = (value: string): string => value.replaceAll("_", " ");
  const qualifier = [precision ? label(precision) : null, certainty ? `${label(certainty)} certainty` : null]
    .filter(Boolean).join(" · ") || null;
  return {
    sourceDate: claim.date_text_original || null,
    qualifier,
    selectionNote: precision === "multi_attestation_broad_range"
      ? "Year selection indexes a broad attestation envelope; it does not establish continuous practice or exact start and end dates."
      : null,
  };
}
