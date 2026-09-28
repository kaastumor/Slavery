import assert from 'node:assert/strict';
import test from 'node:test';
import { claimDateDetail } from './claim-date.ts';

test('broad attestation keeps source date and warns against annual continuity', () => {
  const rendered = claimDateDetail({
    date_text_original: 'Chinese accounts from the third through fifth centuries CE',
    temporal_precision: 'multi_attestation_broad_range',
    temporal_certainty: 'approximate',
  });
  assert.equal(rendered.sourceDate, 'Chinese accounts from the third through fifth centuries CE');
  assert.equal(rendered.qualifier, 'multi attestation broad range · approximate certainty');
  assert.match(rendered.selectionNote, /does not establish continuous practice/);
});

test('exact event has its own date meaning, without broad-range warning', () => {
  const rendered = claimDateDetail({
    date_text_original: '22 June 1633',
    temporal_precision: 'exact_event',
    temporal_certainty: 'high',
  });
  assert.equal(rendered.sourceDate, '22 June 1633');
  assert.equal(rendered.qualifier, 'exact event · high certainty');
  assert.equal(rendered.selectionNote, null);
});

test('legacy payload without qualifiers falls back to numeric interval alone', () => {
  assert.deepEqual(claimDateDetail({}), {
    sourceDate: null,
    qualifier: null,
    selectionNote: null,
  });
});
