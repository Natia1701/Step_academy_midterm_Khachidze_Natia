import os
from pathlib import Path

def get_dictionary_path(filename="dictionary.txt"):
    try: 
        base_dir = Path(__file__).resolve().parent
    except NameError:
        base_dir = Path(os.getcwd())

    file_path = base_dir / filename
    return file_path

#ჩავთვირთოთ მონაცემები ფაილიდან
def load_dictionary(filepath):
    translations = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    source_lang, target_lang, source_word, target_word = parts
                    key = (source_lang.lower().strip(), target_lang.lower().strip(), source_word.lower().strip())
                    translations[key] = target_word.lower().strip()
        return translations
    except FileNotFoundError:
        print(f"Dictionary file '{filepath}' not found.")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}
    
#ინახავს მონაცემებს მეხსიერებაში
def add_translation(dictionary, source_lang, target_lang, source_word, target_word):
    source_lang_lower = source_lang.lower().strip()
    target_lang_lower = target_lang.lower().strip()
    source_word_lower = source_word.lower().strip()
    target_word_stripped = target_word.strip()
    
    key_forward = (source_lang_lower, target_lang_lower, source_word_lower)
    entry_forward = target_word_stripped
    
    key_backward = (target_lang_lower, source_lang_lower, target_word_stripped.lower())
    entry_backward = source_word.strip()

    dictionary[key_forward] = entry_forward
    dictionary[key_backward] = entry_backward
    print(f"The word '{source_word_lower}' -> '{target_word_stripped}' has been added to the dictionary.")

#წერს მონაცემებს არსებულ ფაილში
def save_dictionary(dictionary, filepath):
    sorted_keys = sorted(dictionary.keys()) 
    
    all_lines = []
    for key in sorted_keys:
        source_lang, target_lang, source_word = key
        target_word = dictionary[key]
        
        line = f"{source_lang}|{target_lang}|{source_word}|{target_word}\n"
        all_lines.append(line)
        
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.writelines(all_lines)
        print(f"The translation was added to {filepath} successfully")
    except Exception as e:
        print(f"Error: {e}")
    

#მთავარი ფუნქცია, რომელიც მართავს პროგრამას
def main():
    dictionary_filepath = get_dictionary_path("dictionary.txt")
    dictionary = load_dictionary(dictionary_filepath)
    list_of_lenguages = ['ქართული', 'ინგლისური']

    while True:
        print(f"Available languages: {', '.join(list_of_lenguages)}.")
        question = input("Enter 'yes' if you want to translate, or type 'exit'. ").lower().strip()
        if question == "exit":
            save_dictionary(dictionary, dictionary_filepath) 
            print("Exiting program.")
            break

        if question != "yes":
            print("Invalid input.")
            continue

        while True:
            source_lang_input = input("Please enter source Language: ").lower().strip()
            if source_lang_input not in list_of_lenguages:
                print("Invalid input, please choose language from the list. ")
                continue

            break
        while True:
            target_lang_input = input("Please enter target language: ").lower().strip()
            if target_lang_input not in list_of_lenguages:
                print("Invalid input, please choose language from the list. ")
                continue

            break

        print(f"\n{' '* 4}Translator: {source_lang_input.capitalize()} -> {target_lang_input.capitalize()}")

        while True:
            source_word_input = input("Please enter your word, otherwise type 'exit'. ").lower().strip()
            if source_word_input == "exit":
                break

            if not source_word_input:
                continue

            key  = (source_lang_input, target_lang_input, source_word_input)

            if key in dictionary:
                print(dictionary[key])
            else:
                message = input(f"Your word '{source_word_input}' not found. Do you want to add a translation? (yes/no): ").lower().strip()
                if message == "yes":
                    new_word = input("Please enter translation:").lower().strip()
                    add_translation(
                        dictionary, 
                        source_lang_input, 
                        target_lang_input, 
                        source_word_input, 
                        new_word
                    )
            
    
if __name__ == "__main__":
    main()