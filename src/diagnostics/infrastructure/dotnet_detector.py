from diagnostics.domain.models import DotNetDetection, RepositoryInventory


class DotNetDetector:
    def detect(self, inventory: RepositoryInventory) -> DotNetDetection:
        files = inventory.entries
        projects = tuple(entry.relative_path for entry in files if entry.extension and entry.extension.lower() == ".csproj")
        solutions = tuple(
            entry.relative_path
            for entry in files
            if entry.extension and entry.extension.lower() in {".sln", ".slnx"}
        )
        return DotNetDetection(("dotnet",) if projects or solutions else (), projects, solutions)
