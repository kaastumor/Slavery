from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "web" / "src" / "main.ts").read_text(encoding="utf-8")
WORKFLOW = (ROOT / ".github" / "workflows" / "mvp-health.yml").read_text(encoding="utf-8")
DEPLOY = (ROOT / ".github" / "workflows" / "deploy-pages.yml").read_text(encoding="utf-8")
HEALTH = (ROOT / "tools" / "check_mvp_health.py").read_text(encoding="utf-8")


class MvpAvailabilityGuardrailTests(unittest.TestCase):
    def test_frontend_has_bounded_api_timeout_and_retry(self):
        self.assertIn("fetchApiWithTimeout", MAIN)
        self.assertIn("timeoutMs = 12000", MAIN)
        self.assertIn("controller.abort()", MAIN)
        self.assertIn('id="retry-atlas-load"', MAIN)

    def test_frontend_has_static_snapshot_fallback(self):
        self.assertIn("fetchApiWithFallback", MAIN)
        self.assertIn("./fallback/atlas-data.json", MAIN)
        self.assertIn("static fallback", MAIN)

    def test_pages_deploy_builds_and_retains_snapshot(self):
        self.assertIn("build_public_snapshot.py", DEPLOY)
        self.assertIn("published-release-snapshot-", DEPLOY)
        self.assertIn("Verify deployed static snapshot", DEPLOY)

    def test_monitor_runs_every_fifteen_minutes(self):
        self.assertIn('cron: "*/15 * * * *"', WORKFLOW)

    def test_monitor_checks_api_and_site(self):
        self.assertIn("check_mvp_health.py", WORKFLOW)
        self.assertIn("dilnayfllygkplsdymel.supabase.co/functions/v1/atlas-data", WORKFLOW)
        self.assertIn("kaastumor.github.io/Slavery/", WORKFLOW)

    def test_monitor_opens_and_closes_incident_issue(self):
        self.assertIn("[monitor] MVP availability degraded", WORKFLOW)
        self.assertIn("Open or update outage issue", WORKFLOW)
        self.assertIn("Close outage issue after recovery", WORKFLOW)

    def test_health_check_validates_release_shape_and_latency(self):
        self.assertIn("max-api-seconds", HEALTH)
        self.assertIn("release_version", HEALTH)
        self.assertIn("release_channel", HEALTH)
        self.assertIn("place_count", HEALTH)
        self.assertIn("claim_count", HEALTH)
        self.assertIn("places", HEALTH)
        self.assertIn("cartography", HEALTH)


if __name__ == "__main__":
    unittest.main()
