git
	branches :
		main → dernière version stable
			on code jamais directement dessus.
		dev
			c'est là qu'on code.

	worktree
		deux dossiers :
			~/code/anki → branche main

			~/code/anki_dev → branche dev

	pour lancer la dernière version stable,
	aller dans ~/code/anki et lancer la bonne commande make
		si on veut rester dans le dossier de dev,
		faire un commit puis "git switch main"

	pour valider les changements de dev,
	aller sur la branche main ("git switch main" ou aller dans ~/code/anki) puis :
	git merge dev

config dans les .env, makefile et src/define.py

makefile
	make add (la règle par défaut)
		ça traite input.txt et le dossier images
		pour ajouter des cartes à anki et formater les cartes MosaLingua

		ça déplace les images (qui sont utilisées dans l'input)

		ça envoie à la corbeille les images non utilisées

		ça reset l'input (mais ça garde le backup des 10 derniers inputs traités)
		et ça met l'output de MosaLingua dedans

	make get
		ça récupère les cartes enfouies et marquées dans l'input,
		ça les met dans le deck poubelle,
		et ça archive le deck poubelle

	on peut lancer la prod depuis un autre dossier avec :
		make -C ~/code/anki ENV=prod add
		make -C ~/code/anki ENV=prod get
