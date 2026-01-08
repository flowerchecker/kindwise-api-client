import unasync
import os
from pathlib import Path


def post_process(filepath):
    """
    Manually fixes imports that unasync's token matching cannot handle.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # FIX 1: Rewrite the dotted import path
    # Turns "from kindwise.async_api.core" -> "from kindwise.core"
    content = content.replace("kindwise.async_api", "kindwise")

    # FIX 2: Ensure any leftover relative imports are correct (if needed)
    # content = content.replace("... something else ...", "...")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    gt_code_dir = Path(__file__).resolve().parent.parent / 'kindwise' / 'async_api'
    filepaths = [path for path in gt_code_dir.glob('*.py') if path.stem != '__init__']
    rules = [
        unasync.Rule(
            fromdir="/kindwise/async_api",
            todir="/kindwise",
            additional_replacements={
                "AsyncClient": "Client",
                "AsyncKindwiseApi": "KindwiseApi",
                "anyio": "pathlib",
                "AsyncInsectApi": "InsectApi",
                "AsyncMushroomApi": "MushroomApi",
                "AsyncCropHealthApi": "CropHealthApi",
                "AsyncPlantApi": "PlantApi",
            },
        )
    ]

    filepaths_to_process = [os.path.abspath(p) for p in filepaths]
    unasync.unasync_files(filepaths_to_process, rules)
    for path in filepaths:
        post_process(path.parent.parent / path.name)


if __name__ == "__main__":
    main()
