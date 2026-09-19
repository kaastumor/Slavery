from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "zotero"))

from crosswalk import zotero_attachment_to_asset_candidate, zotero_item_to_source_candidate  # noqa: E402


class ZoteroCrosswalkTests(unittest.TestCase):
    def test_bibliographic_item_never_becomes_reviewed_version(self):
        item = {
            "key": "ABC123",
            "version": 42,
            "data": {
                "itemType": "journalArticle",
                "title": "Example historical article",
                "creators": [{"creatorType": "author", "firstName": "Ada", "lastName": "Historian"}],
                "publicationTitle": "Example Journal",
                "date": "2020",
                "DOI": "10.1234/example",
                "url": "https://example.org/article",
            },
        }
        result = zotero_item_to_source_candidate(item)
        self.assertFalse(result["canonical_write_allowed"])
        self.assertEqual(result["source_candidate"]["external_identifiers"]["zotero_item_key"], "ABC123")
        self.assertEqual(
            result["source_version_candidate"]["status"],
            "candidate_needs_exact_version_review",
        )

    def test_attachment_requires_asset_review(self):
        item = {
            "key": "ATT1",
            "version": 9,
            "data": {
                "itemType": "attachment",
                "parentItem": "ABC123",
                "title": "PDF",
                "contentType": "application/pdf",
                "filename": "paper.pdf",
            },
        }
        result = zotero_attachment_to_asset_candidate(item)
        self.assertFalse(result["canonical_write_allowed"])
        self.assertEqual(result["status"], "asset_candidate_needs_checksum_and_rights_review")


if __name__ == "__main__":
    unittest.main()
