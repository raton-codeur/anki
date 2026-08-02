branche main : stable

on code sur la branche dev, jamais sur main

pour lancer la dernière version stable
	faire un commit du travail en cours sur dev,
	"git switch main",
	lancer le script,
	"git switch dev"

pour mettre à jour la version stable / valider les changement de dev
	"git switch main"
	"git merge dev"
	"git merge dev"



commandes utiles :
- revenir à
- git switch main (faire un commit du travail en cours sur dev si besoin)
- git merge dev (quand on est sur main, pour mettre à jour la version stable



voir la config dans le makefile et src/define.py

repo de dev dans ~/code/anki_dev

repo de prod dans ~/code/anki_stable
	on le lance avec "make prod -C ~/code/anki_stable"
	depuis ~/Documents/anki
