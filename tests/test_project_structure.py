import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("timeboxed-delivery", "wait-discipline", "batch-concurrency")


class ProjectStructureTests(unittest.TestCase):
    def test_plugin_manifests_are_valid_json(self):
        for relative in (
            ".codex-plugin/plugin.json",
            ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
        ):
            with self.subTest(relative=relative):
                json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_shared_defaults_schema_and_required_keys(self):
        data = json.loads(
            (ROOT / "skills/_shared/agent-execution-defaults.json").read_text(
                encoding="utf-8"
            )
        )
        for key in (
            "schema_version",
            "timeboxed_delivery",
            "wait_discipline",
            "remote_model_api",
            "parallel_programming",
            "async_programming",
        ):
            self.assertIn(key, data)

        self.assertEqual(
            data["timeboxed_delivery"]["default_deadline_warning_seconds"], 30
        )
        self.assertTrue(
            data["timeboxed_delivery"]["prefer_subagent_execution_when_available"]
        )
        self.assertTrue(data["wait_discipline"]["ban_hidden_multi_minute_sleep"])
        self.assertEqual(data["parallel_programming"]["default_processes"], 16)
        self.assertGreaterEqual(data["remote_model_api"]["default_tpm_limit"], 1)
        self.assertGreaterEqual(data["remote_model_api"]["default_rpm_limit"], 1)

    def test_skill_frontmatter(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                path = ROOT / "skills" / skill / "SKILL.md"
                text = path.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                frontmatter = text.split("---\n", 2)[1]
                fields = {}
                for line in frontmatter.splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        fields[key.strip()] = value.strip()
                self.assertEqual(fields.get("name"), skill)
                self.assertGreater(len(fields.get("description", "")), 80)
                self.assertRegex(fields["name"], r"^[a-z0-9-]+$")

    def test_all_markdown_has_language_link(self):
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                if path.name.endswith(".zh.md") or path.name == "README.zh.md":
                    self.assertIn("[English]", text)
                else:
                    self.assertIn("[中文版]", text)

    def test_language_counterparts_exist(self):
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts or path.name.endswith(".zh.md"):
                continue
            counterpart = path.with_name(path.stem + ".zh.md")
            if path.name == "README.md":
                counterpart = ROOT / "README.zh.md"
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(counterpart.exists(), f"missing {counterpart}")

    def test_readme_links_exist(self):
        for readme in (ROOT / "README.md", ROOT / "README.zh.md"):
            text = readme.read_text(encoding="utf-8")
            links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
            for link in links:
                if "://" in link:
                    continue
                target = (readme.parent / link).resolve()
                with self.subTest(readme=readme.name, link=link):
                    self.assertTrue(target.exists(), f"broken link: {link}")

    def test_eval_docs_have_metrics_success_and_failure(self):
        for skill in SKILLS:
            for suffix, expected_terms in (
                ("-evals.md", ("## Metrics", "Success:", "Failure:")),
                ("-evals.zh.md", ("## 指标", "成功：", "失败：")),
            ):
                path = ROOT / "docs" / f"{skill}{suffix}"
                with self.subTest(path=path.relative_to(ROOT)):
                    text = path.read_text(encoding="utf-8")
                    for term in expected_terms:
                        self.assertIn(term, text)
                    self.assertGreaterEqual(text.count("### "), 6)

    def test_install_scripts_have_bash_syntax(self):
        for script in (
            "scripts/install-codex-skills.sh",
            "scripts/install-claude-skills.sh",
            "scripts/validate.sh",
        ):
            with self.subTest(script=script):
                subprocess.run(
                    ["bash", "-n", str(ROOT / script)],
                    check=True,
                    cwd=ROOT,
                )


if __name__ == "__main__":
    unittest.main()
