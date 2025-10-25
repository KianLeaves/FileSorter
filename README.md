What you should do:

Simply copy all the pictures, videos, etc., that you have into the "Unsorted Dump" folder. The rest will be sorted by the sort.py program when I run it.
Theoretically, that's it. :)



If you want to organize things yourself:


Optimizing folders for pictures (Windows) [otherwise it will probably be a bit slow for you]:

To be able to view your photos in the folder as thumbnails as efficiently and quickly as possible, Windows offers a function that "optimizes" the folder "for pictures". Here's how to activate it:
⦁ Open the folder (e.g., the "Photos" folder on your NAS).
⦁ Right-click in an empty area and select "Properties".
⦁ Switch to the "Customize" tab.
⦁ Under "Optimize this folder for:", select "Pictures" from the dropdown menu.
⦁ Click "Apply" and then "OK".

This will automatically display larger thumbnails in this folder and allow Windows to display the image files better and faster. Don't worry – this setting only affects your computer and doesn't change anything about the files or the NAS. Other family members will still see their own view.



Important!!!

Please do not rename any of the existing YYYY or YYYY.MM folders, as the program uses them for sorting!



Special folders:

If you want special folders, e.g., for weddings, then create them yourself using the following scheme:

YYYY.MM.DD - "Name"

and then place them in the correct location...



More information about the program (sort.py)

How does the program work?
⦁ The program searches all files in the "Unsorted Dump" folder on the NAS.
⦁ Files with photo file extensions (e.g., .jpg, .png, .heic, etc.) are moved to the Photos folder.
⦁ Files with video file extensions (e.g., .mp4, .mov, .mkv, etc.) are moved to the Videos folder. • All other files (e.g., documents) remain in the Unsorted Dump folder and are not moved.
• Within the Photos and Videos folders, files are sorted into subfolders by year (YYYY) and month (YYYY.MM) based on their modification date.
• Folders are only created if at least one file is placed in them, thus preventing the creation of empty folders.
• If a file with the same name already exists in the destination folder, its contents are compared:
• If the files are identical, the existing file is overwritten by the new one.
• If the files are different, the new file is given a +1, +2, etc. suffix to its filename to avoid naming conflicts.



Supported file types

Photos:
.jpg, .jpeg, .png, .gif, .bmp, .tiff, .heic, .raw, .arw, .svg, .webp, .dp, .pdn

Videos:
.mp4, .mov, .avi, .mkv, .flv, .wmv, .mpeg, .mpg, .3gp, .m4v, .webm, .vob, .mts


Files such as documents (.pdf, .docx, etc.) or other file types remain in the Unsorted Dump folder and are not moved.






__________________________________________________
CMD commands if Files are on Desktop:
cd Desktop
python3 sort.py

July 30, 2025
