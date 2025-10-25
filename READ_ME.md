## **Was ihr tun sollt:**



Alle Bilder, Videos etc., die ihr habt, einfach in den Ordner "Unsorted Dump" kopieren. Den Rest sortiert das sort.py Programm, wenn ich es starte.

Theoretisch wars das. :)







## **Falls ihr selber Ordnung schaffen wollt:**





### Ordner für Bilder optimieren (Windows)\[sonst ist es vermutlich etwas langsam bei euch]:



Um eure Fotos im Ordner möglichst gut und schnell als Vorschaubilder (Thumbnails) sehen zu können, bietet Windows eine Funktion, die den Ordner „für Bilder optimiert“. So aktiviert ihr das:

* Öffnet den Ordner (z.B. den „Photos“-Ordner auf eurem NAS).
* Klickt mit der rechten Maustaste in einen freien Bereich und wählt „Eigenschaften“.
* Wechselt zum Reiter „Anpassen“.
* Unter „Diesen Ordner optimieren für:“ wählt ihr aus dem Dropdown-Menü „Bilder“ aus.
* Klickt auf „Übernehmen“ und dann „OK“.



Dadurch zeigt Windows in diesem Ordner automatisch größere Vorschaubilder und kann die Bilddateien besser und schneller darstellen. Keine Sorge – diese Einstellung wirkt nur auf euren Computer und ändert nichts an den Dateien oder dem NAS. Andere Familienmitglieder sehen weiterhin ihre eigene Ansicht.







### **Wichtig!!!**



Bitte keine der bestehenden Ordner YYYY oder YYYY.MM umbenennen, da das Programm diese zur Sortierung nutzt!







### Besondere Ordner:



Wenn ihr spezielle Ordner wollt, z.B. für Hochzeiten, dann erstellt diese selbst mit folgendem Schema:



YYYY.MM.TT - "Name"



und diesen halt richtig einordnen...







## Mehr Infos uber das Programm (sort.py)



### Wie funktioniert das Programm?

* Das Programm durchsucht alle Dateien im Ordner "Unsorted Dump" auf dem NAS.
*  	Dateien mit Foto-Dateiendungen (z.B. .jpg, .png, .heic usw.) werden in den Photos-Ordner verschoben.
*  	Dateien mit Video-Dateiendungen (z.B. .mp4, .mov, .mkv usw.) werden in den Videos-Ordner verschoben.
*  	Alle anderen Dateien (z.B. Dokumente) bleiben im Unsorted Dump-Ordner und werden nicht verschoben.
* Innerhalb der Ordner Photos und Videos werden die Dateien anhand ihres Änderungsdatums in Unterordner nach Jahr (YYYY) und Monat (YYYY.MM) sortiert.
* Ordner werden nur dann erstellt, wenn dort mindestens eine Datei landet, so entstehen keine leeren Ordner.
* Existiert im Zielordner bereits eine Datei mit dem gleichen Namen, werden deren Inhalte verglichen:
*  	Sind die Dateien identisch, wird die vorhandene Datei durch die neue überschrieben.
*  	Sind die Dateien unterschiedlich, wird die neue Datei mit einem +1, +2 usw. am Dateinamen versehen, um Namenskonflikte zu vermeiden.







### Unterstützte Dateitypen



Fotos:

.jpg, .jpeg, .png, .gif, .bmp, .tiff, .heic, .raw, .arw, .svg, .webp, .dp, .pdn



Videos:

.mp4, .mov, .avi, .mkv, .flv, .wmv, .mpeg, .mpg, .3gp, .m4v, .webm, .vob, .mts





Dateien wie Dokumente (.pdf, .docx, etc.) oder andere Dateitypen bleiben im Ordner Unsorted Dump und werden nicht verschoben.













\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

CMD:

cd Desktop

python3 sort.py



30.07.2025

