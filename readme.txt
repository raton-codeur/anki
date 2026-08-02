branche stable : main

on code sur la branche dev, jamais sur main

pour lancer la dernière version stable (si on est sur dev),
mieux vaut faire un commit puis :
"git switch main"

pour valider les changement de dev :
"git switch main"
"git merge dev"

le top c'est d'utiliser un worktree :
	~/code/anki
		branche main

		on peut lancer le script depuis ~/Documents/anki
		avec "make -C ~/code/anki"

	~/code/anki_dev
		branche dev

voir la config dans le makefile et src/define.py
