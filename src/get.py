from handle_marked import get_marked, decode_notes, get_back_images, backfill_input, move_marked_cards
from utils import get_trashed_cards, update_anki_trash
from handle_spotify import get_songs, handle_spotify, copy_songs_to_input

def get():
    marked_card_ids, marked_notes = get_marked()
    # marked_notes est une liste de dictionnaires des cartes marquées sur Anki
    # dont les clés sont : separator, fields
    if marked_notes:
        print(f"{len(marked_notes)} notes récupérées")

        marked_notes = decode_notes(marked_notes)
        # les notes marquées sont maintenant décodées.

        get_back_images(marked_notes)
        # on a récupéré les images des cartes marquées.

        backfill_input(marked_notes)
        # on a récupéré les cartes marquées dans l'input.

        move_marked_cards(marked_card_ids)

    trashed_note_ids = get_trashed_cards()
    if trashed_note_ids:
        print(f"{len(trashed_note_ids)} notes retirées d'Anki")

        update_anki_trash(trashed_note_ids)
        # la poubelle d'Anki a été vidée.

    songs = get_songs()
    if songs:
        handle_spotify(songs)
    copy_songs_to_input(songs)
