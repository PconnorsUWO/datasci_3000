from quiz import gen_flashcards, generate_unique_id
import genanki

if __name__ == '__main__':

    anki_model = genanki.Model(
        generate_unique_id(), 
        'my format',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}', 
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}', 
            },
        ],
        css='''
        .card {
            font-family: Arial, sans-serif;
            font-size: 20px;
            text-align: left;
            color: black;
            background-color: white;
        }
        '''
    )

    gen_flashcards("week5.txt","ds3000_week5.apkg","ds3000_week5", anki_model=anki_model)