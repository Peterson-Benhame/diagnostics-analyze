from diagnostics.domain.models import EntryKind, InventoryEntry, RepositoryInventory
from diagnostics.infrastructure.dotnet_detector import DotNetDetector


def test_detector_finds_projects_and_solution_signals_case_insensitively() -> None:
    inventory = RepositoryInventory(
        "sample",
        (
            InventoryEntry("src/A/A.CSPROJ", EntryKind.FILE, ".csproj"),
            InventoryEntry("sample.sln", EntryKind.FILE, ".sln"),
            InventoryEntry("sample.SLNX", EntryKind.FILE, ".slnx"),
        ),
        (),
        (),
        3,
        False,
    )

    assert DotNetDetector().detect(inventory).project_files == ("src/A/A.CSPROJ",)
    assert DotNetDetector().detect(inventory).solution_files == ("sample.sln", "sample.SLNX")
    assert DotNetDetector().detect(inventory).stack_signals == ("dotnet",)
