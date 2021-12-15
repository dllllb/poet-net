import logging
from transformers import FSMTTokenizer, FSMTForConditionalGeneration
from typing import List
import argparse


SAVE_ITERATION = 10000


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger("parallel corpus generator")


class PhraseTransformer:
    def __init__(self, ru_en_model: str, en_ru_model: str, device: str):
        self.device = device
        self.tokenizer_ru_en = FSMTTokenizer.from_pretrained(ru_en_model)
        self.tokenizer_en_ru = FSMTTokenizer.from_pretrained(en_ru_model)
        self.model_ru_en = FSMTForConditionalGeneration.from_pretrained(ru_en_model).to(device)
        self.model_en_ru = FSMTForConditionalGeneration.from_pretrained(en_ru_model).to(device)

    def transform_batch(self, data: List[str]) -> List[str]:
        ru_tokens = self.tokenizer_ru_en(data, return_tensors="pt",
                                         truncation=True, padding="longest")['input_ids'].to(self.device)
        transformed_phrases = self.model_ru_en.generate(input_ids=ru_tokens)
        translation = self.tokenizer_ru_en.batch_decode(transformed_phrases, skip_special_tokens=True)
        en_tokens = self.tokenizer_en_ru(translation, return_tensors="pt",
                                         truncation=True, padding="longest")['input_ids'].to(self.device)
        return self.tokenizer_en_ru.batch_decode(en_tokens, skip_special_tokens=True)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--poetry_data_location", type=str)
    parser.add_argument("--prose_poetry_file_location", type=str)
    parser.add_argument("--device", type=str, default='cpu')
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--ru_en_model", type=str, default="facebook/wmt19-ru-en")
    parser.add_argument("--en_ru_model", type=str, default="facebook/wmt19-en-ru")
    return parser.parse_args()


def read_data(data_location: str) -> List[str]:
    logger.info("Start data reading")
    data = []
    with open(data_location) as data_file:
        for line in data_file:
            data.append(line.replace('\\n', '\n'))
    logger.info(f"Total object counts {len(data)}")
    logger.info("Finished data reading")
    return data


def init_data_file(data_location):
    with open(data_location, 'w') as data_file:
        data_file.write("prose\tpoetry\n")


def save_data_batch(data_batch, data_location):
    with open(data_location, 'a') as data_file:
        for poetry, prose in data_batch:
            data_file.write(f"{prose}\t{poetry}\n")


def process_data(data: List[str], text_transformer: PhraseTransformer, transformed_data_location: str, batch_size: int):
    init_data_file(transformed_data_location)
    logger.info("Start data generation")
    current_batch = []
    current_pairs = []
    for index, elem in enumerate(data):
        if len(current_batch) < batch_size and index < len(data):
            current_batch.append(elem)
        else:
            prose_text = text_transformer.transform_batch(current_batch)
            current_pairs.extend(zip(prose_text, current_batch))
        if index % SAVE_ITERATION == 0 or index == len(data) - 1:
            save_data_batch(current_pairs, transformed_data_location)
            current_pairs = []
            logger.info(f"Save {index+1}/{len(data)} prose poetry pairs")


def main():
    args = get_args()
    poetry_data = read_data(args['poetry_data_location'])
    text_transformer = PhraseTransformer(args['ru_en_model'], args['en_ru_model'], args['device'])
    process_data(poetry_data, text_transformer, args['prose_poetry_file_location'],  args['batch_size'])


if __name__ == '__main__':
    main()