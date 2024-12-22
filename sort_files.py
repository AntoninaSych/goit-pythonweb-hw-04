import argparse
import asyncio
import aiofiles
import logging
from pathlib import Path
import shutil

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("file_sorter.log"),
        logging.StreamHandler()
    ]
)

# Асинхронна функція для створення папки за розширенням
async def ensure_folder(output_folder: Path, extension: str):
    target_folder = output_folder / extension.lstrip('.')
    target_folder.mkdir(parents=True, exist_ok=True)
    return target_folder


# Асинхронне копіювання файлу
async def copy_file(file: Path, target_folder: Path):
    try:
        target_path = target_folder / file.name
        shutil.copy(file, target_path)
        logging.info(f"Copied: {file} → {target_path}")
    except Exception as e:
        logging.error(f"Failed to copy {file}: {e}")


# Асинхронне читання папки
async def read_folder(source_folder: Path, output_folder: Path):
    tasks = []

    for file in source_folder.rglob('*'):
        if file.is_file():
            extension = file.suffix.lower() or "no_extension"
            target_folder = await ensure_folder(output_folder, extension)
            tasks.append(copy_file(file, target_folder))

    if tasks:
        await asyncio.gather(*tasks)


# Основна функція
async def main():
    parser = argparse.ArgumentParser(description="Asynchronously sort files by extension.")
    parser.add_argument('source', type=str, help="Source folder path")
    parser.add_argument('output', type=str, help="Output folder path")
    args = parser.parse_args()

    source_folder = Path(args.source)
    output_folder = Path(args.output)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error("Source folder does not exist or is not a directory.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)
    await read_folder(source_folder, output_folder)
    logging.info("File sorting completed successfully.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.warning("Process interrupted by user.")
