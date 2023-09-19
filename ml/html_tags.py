import torch
from transformers import GPT2Tokenizer, T5ForConditionalGeneration
import locale
import re
from os.path import dirname
locale.getpreferredencoding = lambda: "UTF-8"

path_to_weights = f"{dirname(__file__)}/model/checkpoint-html/"

tokenizer = GPT2Tokenizer.from_pretrained('ai-forever/FRED-T5-large',eos_token='</s>')
tokenizer.add_special_tokens({'bos_token': '<s>', 'eos_token': '</s>', 'pad_token': '<pad>'})
model = T5ForConditionalGeneration.from_pretrained(path_to_weights)


def remove_tags(input_string):
    # Define a pattern to match <pad>, </s>, and <s> tags
    pattern = r'<\/?s>|<pad>'

    # Use re.sub() to replace all matches with an empty string
    cleaned_string = re.sub(pattern, '', input_string)
    cleaned_string = cleaned_string.replace('html:','').replace('html','').replace('pad','')

    return cleaned_string


def add_html_tags(text):
    lm_text = ('<LM> Исправь ошибки, добавь HTML тэги: '.lower() + text + ' HTML: '.lower())
    input_ids = torch.tensor([tokenizer.encode(lm_text, truncation=True, max_length=256)])
    outputs = model.generate(input_ids, max_length=160, early_stopping=False)
    s = tokenizer.decode(outputs[0][:])
    s = remove_tags(s)

    return s