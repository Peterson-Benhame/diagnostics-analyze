from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_spec_driven_feature_layout_has_active_feature_artifacts() -> None:
    expected_paths = (
        ".specs/STATE.md",
        ".specs/features/f001-inventory/spec.md",
        ".specs/features/f002-ai-workflow/spec.md",
        ".specs/features/f002-ai-workflow/tasks.md",
        ".specs/features/f002-ai-workflow/validation.md",
    )

    missing_paths = [path for path in expected_paths if not (PROJECT_ROOT / path).is_file()]

    assert missing_paths == []


def test_state_references_feature_directory_with_required_artifacts() -> None:
    state = (PROJECT_ROOT / ".specs/STATE.md").read_text(encoding="utf-8")
    active_feature = re.search(r"^- Diretório: `(.+?)/`$", state, flags=re.MULTILINE)

    assert active_feature is not None
    feature_directory = PROJECT_ROOT / active_feature.group(1)
    assert (feature_directory / "spec.md").is_file()
    assert (feature_directory / "tasks.md").is_file()
    assert (feature_directory / "validation.md").is_file()


def test_agent_entrypoint_requires_state_active_feature_and_validation() -> None:
    agent_instructions = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert ".specs/STATE.md" in agent_instructions
    assert "feature ativa" in agent_instructions
    assert "validation.md" in agent_instructions
    assert "context.md" in agent_instructions
    assert "design.md" in agent_instructions
    assert "Verifier independente" in agent_instructions


def test_feature_specs_preserve_source_and_design_references() -> None:
    inventory_spec = (PROJECT_ROOT / ".specs/features/f001-inventory/spec.md").read_text(
        encoding="utf-8"
    )
    workflow_spec = (PROJECT_ROOT / ".specs/features/f002-ai-workflow/spec.md").read_text(
        encoding="utf-8"
    )

    assert "PRD-001-diagnostico-tecnico-dotnet.md" in inventory_spec
    assert "2026-09-26-ai-assisted-development-workflow-design.md" in workflow_spec
    assert "2026-09-26-pbs-spec-driven-workflow.md" in workflow_spec


def test_local_skill_setup_documents_required_skills_and_limits() -> None:
    skill_setup = (PROJECT_ROOT / ".agents/skills/README.md").read_text(encoding="utf-8")

    assert "pbs-spec-driven" in skill_setup
    assert "harness-eval" in skill_setup
    assert "security-best-practices" in skill_setup
    assert "instalação global" in skill_setup
    assert "MCP é opcional" in skill_setup
    assert "não são copiados" in skill_setup
    assert "não bloqueia a conclusão" in skill_setup
