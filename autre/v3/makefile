sas_path = '/Users/quentinhauuy/Documents/à apprendre/sas.txt'
images_src_dir = /Users/quentinhauuy/Downloads
images_dst_dir = "/Users/quentinhauuy/Library/Application Support/Anki2/Quentin/collection.media"
output_dir = out
log_dir = log

test :
	@ reset
	@ source repo/venv/bin/activate && python3 repo/main.py $(sas_path) $(images_src_dir) $(images_dst_dir) $(output_dir) $(log_dir)

i :
	open "/Users/quentinhauuy/Library/Application Support/Anki2/Quentin/collection.media"

a :
	open "/Users/quentinhauuy/Documents/à apprendre/"