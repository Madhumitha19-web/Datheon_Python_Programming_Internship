"""Organize files in a selected folder by extension (Python 3, standard library)."""

import os
import shutil
from pathlib import Path

CATEGORIES = {
    'Documents': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.csv', '.xls', '.xlsx', '.ppt', '.pptx'},
    'Images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'},
    'Videos': {'.mp4', '.mov', '.avi', '.mkv', '.webm'},
    'Archives': {'.zip', '.rar', '.7z', '.tar', '.gz'},
    'Code': {'.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.json'},
    'Audio': {'.mp3', '.wav', '.flac', '.aac'},
}


def category_for(filename):
    extension = Path(filename).suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return 'Others'


def unique_destination(folder, filename):
    destination = folder / filename
    counter = 1
    while destination.exists():
        source_name = Path(filename)
        destination = folder / f'{source_name.stem}_{counter}{source_name.suffix}'
        counter += 1
    return destination


def organize(folder):
    moved = skipped = failed = 0
    print(f'\nOrganizing: {folder}\n')
    try:
        with os.scandir(folder) as entries:
            for entry in entries:
                try:
                    if not entry.is_file(follow_symlinks=False):
                        skipped += 1
                        continue
                    source = Path(entry.path)
                    if source.resolve() == Path(__file__).resolve():
                        print(f'SKIPPED (running script): {source.name}')
                        skipped += 1
                        continue
                    target_folder = folder / category_for(source.name)
                    target_folder.mkdir(exist_ok=True)
                    destination = unique_destination(target_folder, source.name)
                    shutil.move(str(source), str(destination))
                    print(f'MOVED: {source.name} -> {destination.relative_to(folder)}')
                    moved += 1
                except (PermissionError, FileExistsError, OSError) as error:
                    print(f'FAILED: {entry.name} ({error})')
                    failed += 1
    except (PermissionError, OSError) as error:
        print(f'Cannot scan folder: {error}')
        return
    print('\n===== EXECUTION SUMMARY =====')
    print(f'Files moved  : {moved}')
    print(f'Items skipped: {skipped}')
    print(f'Files failed : {failed}')
    print('=============================')


def main():
    print('=== Automated File Organizer ===')
    print('Tip: Test on a COPY of a folder first; files will be moved.')
    raw_path = input('Enter folder path: ').strip().strip('"').strip("'")
    folder = Path(raw_path).expanduser()
    if not folder.is_dir():
        print('Error: Folder does not exist.')
        return
    confirmation = input(f'Move files inside "{folder}"? (yes/no): ').strip().lower()
    if confirmation != 'yes':
        print('Cancelled. No files were moved.')
        return
    organize(folder)


if __name__ == '__main__':
    main()
