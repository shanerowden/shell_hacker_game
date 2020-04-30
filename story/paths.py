from pathlib import Path

class Pathing:
    paths = {
        'mission1phase1-clock.md': Path('mission1phase1-clock.md').resolve(),
    }

    @classmethod
    def verify_paths(cls):
        for path in cls.paths.values():
            if not path.exists():
                raise FileNotFoundError(f"Missing File: {path}")
            else:
                print("Paths are good.")