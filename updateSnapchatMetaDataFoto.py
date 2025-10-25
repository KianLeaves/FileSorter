import os
import re
import exiftool

def parse_date_from_filename(filename):
    # Matches date pattern YYYY-MM-DD at start of filename
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", filename)
    if not match:
        return None
    year, month, day = match.groups()
    return f"{year}:{month}:{day} 00:00:00"  # EXIF date format

def set_metadata_dates(directory):
    with exiftool.ExifTool() as et:
        for fname in os.listdir(directory):
            fpath = os.path.join(directory, fname)
            date_str = parse_date_from_filename(fname)
            if not date_str:
                continue  # skip if date not in filename
            
            tags = {
                'DateTimeOriginal': date_str,
                'CreateDate': date_str,
                'MediaCreateDate': date_str,
            }
            try:
                et.execute(
                    "-overwrite_original",
                    *[f"-{k}={v}" for k, v in tags.items()],
                    fpath
                )
                print(f"Updated metadata date for {fname} to {date_str}")
            except Exception as e:
                print(f"Failed to update {fname}: {e}")

if __name__ == "__main__":
    dump_dir = r"\\TRUENAS\Photos_and_Videos\Unsorted Dump"
    set_metadata_dates(dump_dir)
