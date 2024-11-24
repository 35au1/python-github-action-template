import json
from googletrans import Translator

def translate_json(file_path, output_path):
    # Initialize the translator
    translator = Translator()
    
    # Load the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate through the data and translate the 'body' content
    for item in data:
        if 'body' in item:
            for key, value in item['body'].items():
                if isinstance(value, str):
                    # Translate text to Polish
                    translated = translator.translate(value, src='en', dest='pl')
                    item['body'][key] = translated.text
    
    # Save the translated JSON to a new file
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Paths
input_file = "ufonews.json"  # Replace with your input file path
output_file = "translated_ufonews.json"  # Output file path

# Run the translation
translate_json(input_file, output_file)
print(f"Translation completed. Translated file saved as {output_file}")
