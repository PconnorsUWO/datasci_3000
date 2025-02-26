import genanki
import random
import ast

def generate_unique_id():
    return random.randrange(1 << 30, 1 << 31)

def gen_flashcards(input_file: str, output_file: str, deck_name: str, anki_model) -> None:
    anki_deck = genanki.Deck(
        generate_unique_id(),
        deck_name
    )

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
            if not file_content.strip().startswith('['):
                file_content = f'[{file_content}]'
            questions_and_answers = ast.literal_eval(file_content)
    except Exception as e:
        print(f"An error occurred while reading the input file: {e}")
        return

    for qa in questions_and_answers:
        try:
            question = qa['question']
            answer = qa['answer']
        except KeyError as e:
            print(f"Missing key in QA: {e}")
            continue

        note = genanki.Note(
            model=anki_model,
            fields=[question, answer]
        )
        anki_deck.add_note(note)

    try:
        genanki.Package(anki_deck).write_to_file(output_file)
        print(f"Anki deck created and saved as {output_file}")
    except Exception as e:
        print(f"An error occurred while creating the Anki deck: {e}")






