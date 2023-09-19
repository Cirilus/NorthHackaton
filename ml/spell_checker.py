# Импортируем библиотеки
from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast
import torch
# Зададим название выбронной модели из хаба
MODEL_NAME = 'UrukHan/t5-russian-spell'
MAX_INPUT = 256

# Загрузка модели и токенизатора
spell_tokenizer = T5TokenizerFast.from_pretrained(MODEL_NAME)
spell_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


model, example_texts, languages, punct, apply_te = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                  model='silero_te')

import re


def process_string_with_tags(input_string):
    # Define a regular expression pattern to match tags in the input string
    tag_pattern = r'<[^>]+>'
    new_segments = []

    # Find all tags in the input string and store them in a list
    tags = re.findall(tag_pattern, input_string)

    # Split the input string into segments based on the tags
    segments = re.split(tag_pattern, input_string)

    # Perform your desired operations on the text segments (e.g., adding punctuation and capitalization)
    input_sequences = segments  # ['сеглдыя хорош ден', 'когд а вы прдет к нам в госи']   # или можно использовать одиночные фразы:  input_sequences = 'сеглдыя хорош ден'

    task_prefix = "Spell correct: "  # Токенизирование данных
    if type(input_sequences) != list: input_sequences = [input_sequences]
    encoded = spell_tokenizer(
        [task_prefix + sequence for sequence in input_sequences],
        padding="longest",
        max_length=MAX_INPUT,
        truncation=True,
        return_tensors="pt",
    )

    predicts = spell_model.generate(**encoded)  # # Прогнозирование
    new_segments = spell_tokenizer.batch_decode(predicts, skip_special_tokens=True)  # Декодируем данные

    # Add a period to each segment

    # Initialize an empty processed string
    processed_text = ''

    # Reconstruct the processed text by interleaving segments and tags
    for i in range(len(segments)):
        processed_text += new_segments[i]
        if i < len(tags):
            processed_text += tags[i]

    return processed_text.replace('...', '').replace(' : ', '').replace('::', '')

def capitalize_first_cyrillic(text):
    lines = text.split("\n")
    capitalized_lines = []

    for line in lines:
        # Find the first Cyrillic letter using regular expression
        match = re.search(r'[а-яА-Я]', line)
        if match:
            first_cyrillic_letter = match.group(0)
            # Capitalize the first Cyrillic letter and replace it in the line
            line = line.replace(first_cyrillic_letter, first_cyrillic_letter.upper(), 1)
        capitalized_lines.append(line)

    return "\n".join(capitalized_lines)


def check_spell(text):
    text = process_string_with_tags(text)
    text = capitalize_first_cyrillic(text)
    return text
