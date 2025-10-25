import os
import re
import datetime
import tempfile
import concurrent.futures
import pywintypes
import win32file
import win32con
from exiftool import ExifTool

# === CONFIG ===
DUMP_DIR = r"\\TRUENAS\Photos_and_Videos\Unsorted Dump"
RECURSIVE = False
THREADS = 8  # number of threads to set Windows creation time
LOG_FILE = True

DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})_")
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".mts", ".m2ts", ".3gp", ".wmv"}

def parse_date_from_filename(filename):
    m = DATE_RE.match(filename)
    if not m:
        return None
    year, month, day = m.groups()
    return datetime.datetime(int(year), int(month), int(day), 0, 0, 0)

def is_video_file(path):
    return os.path.splitext(path)[1].lower() in VIDEO_EXTS

def collect_video_files(directory, recursive=False):
    all_files = []
    if recursive:
        for root, _, files in os.walk(directory):
            for f in files:
                if is_video_file(f):
                    all_files.append(os.path.join(root, f))
    else:
        for f in os.listdir(directory):
            fpath = os.path.join(directory, f)
            if os.path.isfile(fpath) and is_video_file(f):
                all_files.append(fpath)
    return all_files

def set_file_creation_time(path, dt):
    """Set Windows creation timestamp."""
    try:
        handle = win32file.CreateFile(
            path,
            win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None
        )
        ft = pywintypes.Time(dt)
        win32file.SetFileTime(handle, ft, None, None)  # (creation, access, modified)
        handle.close()
        return True, None
    except Exception as e:
        return False, str(e)

def update_creation_times_parallel(file_dt_list, threads=8):
    """Update Windows creation times in parallel."""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_file = {executor.submit(set_file_creation_time, f, dt): f for f, dt in file_dt_list}
        for future in concurrent.futures.as_completed(future_to_file):
            f = future_to_file[future]
            try:
                success, err = future.result()
                results.append((f, success, err))
            except Exception as e:
                results.append((f, False, str(e)))
    return results

def update_videos(directory):
    files = collect_video_files(directory, RECURSIVE)
    if not files:
        print("No video files found. Exiting.")
        return

    # --- Step 1: Prepare ExifTool argfile for fast batch ---
    arg_file_list = []
    file_dt_list = []  # for Windows creation time update
    skipped_files = []

    for fpath in files:
        fname = os.path.basename(fpath)
        dt = parse_date_from_filename(fname)
        if not dt:
            skipped_files.append(fname)
            continue
        file_dt_list.append((fpath, dt))

        exif_dt = dt.strftime("%Y:%m:%d %H:%M:%S")
        tags = {
            "CreateDate": exif_dt,
            "TrackCreateDate": exif_dt,
            "MediaCreateDate": exif_dt,
            "DateTimeOriginal": exif_dt,
        }
        for k, v in tags.items():
            arg_file_list.append(f"-{k}={v}\n")
            arg_file_list.append(f"-QuickTime:{k}={v}\n")
            if k == "CreateDate":
                arg_file_list.append(f"-XMP:CreateDate={v}\n")
        arg_file_list.append("-overwrite_original\n")
        arg_file_list.append(f"{fpath}\n\n")

    # Write to temp argfile
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".args") as argfile:
        argfile.writelines(arg_file_list)
        arg_path = argfile.name

    print(f"Running ExifTool batch update for {len(file_dt_list)} files...")
    with ExifTool() as et:
        et.execute(f"-@{arg_path}".encode("utf-8"))

    os.remove(arg_path)

    print("ExifTool metadata update completed.\n")

    # --- Step 2: Update Windows creation timestamps in parallel ---
    print(f"Updating Windows creation timestamps using {THREADS} threads...")
    results = update_creation_times_parallel(file_dt_list, THREADS)

    updated_count = sum(1 for _, success, _ in results if success)
    failed_count = sum(1 for _, success, _ in results if not success)

    # --- Summary ---
    print("\n==== SUMMARY ====")
    print(f"Total files processed: {len(files)}")
    print(f"Metadata updated: {len(file_dt_list)}")
    print(f"Windows creation time updated: {updated_count}")
    print(f"Skipped (no date): {len(skipped_files)}")
    print(f"Failed Windows timestamp updates: {failed_count}")
    if skipped_files:
        print(f"Skipped files: {', '.join(skipped_files)}")
    print("=================")

if __name__ == "__main__":
    update_videos(DUMP_DIR)
