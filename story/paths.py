from pathlib import Path

class Pathing:
    PROJECT_ROOT = Path().home().joinpath("Projects", "shell_hacker_game")
    MD_ROOT = PROJECT_ROOT.joinpath("story", "markdown")

    def __init__(self, pattern):
        self.paths = dict()
        self.add_all_paths(pattern)

    def add_all_paths(self, pattern: str):
        md_files = [Path(p) for p in Pathing.MD_ROOT.glob(pattern)]
        print(md_files)
        for p in md_files:
            self._verify_path(p.resolve())
            self._get_path(p.name, p.resolve())

    def _get_path(self, fname_key: str, resolved_path: Path):
        self.paths[fname_key] = resolved_path

    @staticmethod
    def _verify_path(path: Path):
        if not path.exists():
            raise FileNotFoundError(f"Missing File: {path}")
        else:
            print(f"{path.name} confirmed")
