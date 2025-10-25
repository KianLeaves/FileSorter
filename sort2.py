import platform
import filecmp
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
from shutil import move
from PIL import Image, ExifTags


def log(msg: str):
    """Prints timestamped log message."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def extract_zip(zip_path: Path, extract_to: Path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        log(f"✅ Extracted ZIP '{zip_path.name}' to '{extract_to}'")
    except Exception as e:
        log(f"❌ Error extracting ZIP '{zip_path.name}': {e}")


def get_exif_capture_date(file_path: Path):
    """Liest das EXIF-Aufnahmedatum (DateTimeOriginal) aus einem Bild aus, sofern vorhanden."""
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if not exif_data:
            return None

        exif = {
            ExifTags.TAGS.get(tag, tag): value
            for tag, value in exif_data.items()
            if tag in ExifTags.TAGS
        }

        date_str = exif.get('DateTimeOriginal') or exif.get('DateTime')
        if date_str:
            return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        return None
    except Exception:
        return None


def get_creation_time(file: Path) -> float:
    """Gibt Erstellungszeit zurück; Plattformabhängig verwendet sie std. Erstellungs- oder Änderungszeit."""
    if platform.system() == 'Windows':
        return file.stat().st_ctime
    else:
        try:
            return file.stat().st_birthtime  # macOS
        except AttributeError:
            return file.stat().st_mtime    # Linux fallback


def sort_files_by_type_and_date(dump_dir: str):
    dump_path = Path(dump_dir)
    immich_core_dir = dump_path.parent / "Immich_Core"
    photos_dir = immich_core_dir / "Photos"
    videos_dir = immich_core_dir / "Videos"

    photo_exts = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.raw', '.svg', '.webp',
        '.pdn', '.dng', '.arw', '.db'
    }
    video_exts = {
        '.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.mpeg', '.mpg', '.3gp', '.m4v', '.webm', '.vob', '.mts'
    }

    def process_file(file: Path):
        ext = file.suffix.lower()
        if ext in photo_exts:
            base_folder = photos_dir
        elif ext in video_exts:
            base_folder = videos_dir
        else:
            log(f"⚪ Skipped unsupported file: '{file.name}'")
            return

        try:
            # Für Fotos EXIF-Aufnahmedatum versuchen, sonst Erstellungszeit
            if ext in photo_exts:
                dt = get_exif_capture_date(file)
                if dt is None:
                    ctime = get_creation_time(file)
                    dt = datetime.fromtimestamp(ctime)
            else:
                ctime = get_creation_time(file)
                dt = datetime.fromtimestamp(ctime)

            year_folder = base_folder / f"{dt.year}"
            month_folder = year_folder / f"{dt.year}.{dt.month:02d}"

            month_folder.mkdir(parents=True, exist_ok=True)

            dest_file = month_folder / file.name

            if dest_file.exists():
                if filecmp.cmp(file, dest_file, shallow=False):
                    dest_file.unlink()
                    move(str(file), str(dest_file))
                    log(f"🔁 Replaced identical file: '{file.name}' → '{dest_file}'")
                else:
                    counter = 1
                    new_name = f"{file.stem}+{counter}{file.suffix}"
                    new_dest = month_folder / new_name
                    while new_dest.exists():
                        counter += 1
                        new_name = f"{file.stem}+{counter}{file.suffix}"
                        new_dest = month_folder / new_name
                    move(str(file), str(new_dest))
                    log(f"📄 Renamed & moved (conflict): '{file.name}' → '{new_dest}'")
            else:
                move(str(file), str(dest_file))
                log(f"📦 Moved '{file.name}' → '{dest_file}'")

        except Exception as e:
            log(f"❌ Error processing file '{file.name}': {e}")

    def process_path(path: Path):
        if path.is_dir():
            for item in path.iterdir():
                process_path(item)
            if path != dump_path:
                try:
                    path.rmdir()
                    log(f"🗑️ Deleted empty folder: '{path}'")
                except OSError:
                    pass
        elif path.is_file():
            if path.suffix.lower() == '.zip':
                tmp_extract_dir = dump_path / f"_tmp_extract_{path.stem}"
                if tmp_extract_dir.exists():
                    try:
                        shutil.rmtree(tmp_extract_dir)
                        log(f"🧹 Deleted old temp folder: '{tmp_extract_dir}'")
                    except Exception as e:
                        log(f"❌ Error deleting previous temp folder '{tmp_extract_dir}': {e}")

                try:
                    tmp_extract_dir.mkdir()
                    log(f"📁 Created temp extract folder: '{tmp_extract_dir}'")
                except Exception as e:
                    log(f"❌ Error creating temp folder '{tmp_extract_dir}': {e}")

                extract_zip(path, tmp_extract_dir)
                process_path(tmp_extract_dir)

                try:
                    path.unlink()
                    log(f"🗑️ Deleted ZIP file after extraction: '{path.name}'")
                except Exception as e:
                    log(f"❌ Error deleting ZIP '{path.name}': {e}")

                try:
                    if tmp_extract_dir.exists():
                        shutil.rmtree(tmp_extract_dir)
                        log(f"🧹 Cleaned up temp extract folder: '{tmp_extract_dir}'")
                except Exception as e:
                    log(f"❌ Error deleting temp folder '{tmp_extract_dir}': {e}")
            else:
                process_file(path)

    log(f"🚀 Starting sorting in: '{dump_path}'")
    process_path(dump_path)
    log(f"✅ Sorting completed for: '{dump_path}'")


if __name__ == "__main__":
    dump_folder_path = r"\\TRUENAS\Photos_and_Videos\Unsorted Dump"  # Pfad ggf. anpassen
    sort_files_by_type_and_date(dump_folder_path)
