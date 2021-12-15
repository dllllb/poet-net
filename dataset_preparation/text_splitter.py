from rhymetagger import RhymeTagger
from collections import Counter
import argparse
import logging
from typing import List
import json


SAVE_INDEX = 100000


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger("Text splitter")


class TextSplitter:
    def __init__(self):
        self.rhyme_tagger = RhymeTagger()
        self.rhyme_tagger.load_model(model='ru')

    def process_block(self, block: List[str]) -> List[str]:
        all_phrases = []
        rhymes = self.rhyme_tagger.tag(block, output_format=3)
        index = 0
        while index < len(rhymes) - 2:
            rhyme_block = rhymes[index:index + 2]
            if rhyme_block[0] == rhyme_block[1]:
                all_phrases.append("\n".join(block[index:index + 2]))
                index += 1
                continue
            if index < len(rhymes) - 4:
                rhyme_block = rhymes[index:index + 4]
                rhyme_counter = Counter(rhyme_block)
                if len(rhyme_counter) == 2 and rhyme_counter.most_common()[0][1] == 2:
                    all_phrases.append("\n".join(block[index:index + 4]))
                    index += 4
                    continue
            index += 1
        return all_phrases

    def process_text(self, text: str) -> List[str]:
        all_text_blocks = text.split("\n\n")
        all_phrases = []
        for block in all_text_blocks:
            block_splitted = block.split("\n")
            # Assumes all blocks of 2 and 4 lines are rhymed
            if len(block_splitted) in [2, 4]:
                all_phrases.append(block)
            elif len(block_splitted) > 1:
                all_phrases.extend(self.process_block(block_splitted))
        return all_phrases


def save_block(block: List[str], data_location: str):
    with open(data_location, 'a') as data_file:
        for elem in block:
            elem = elem.replace("\n", "\\n")
            data_file.write(f'{elem}\n')


def read_data(data_location: str):
    with open(data_location, "r") as data_file:
        data = json.load(data_file)
    logger.info(f'Load {len(data)} texts to process')
    return data


def process_data(data, new_data_location):
    text_splitter = TextSplitter()
    currently_processed = []
    for index, data_block in enumerate(data):
        currently_processed.extend(text_splitter.process_text(data_block))
        if index % SAVE_INDEX == 0 or index == len(data) - 1:
            logger.info(f"Processed {index+1}/{len(data)} texts")
            save_block(currently_processed, new_data_location)
            currently_processed = []


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_data_location", type=str)
    parser.add_argument("--splitted_dataset_location", type=str)
    parser.parse_args()
    return parser.parse_args()

def main():
    args = get_args()
    data = read_data(args['json_data_location'])
    process_data(data, args['splitted_dataset_location'])
    logger.info(f"Finish data processing. Location {args['splitted_dataset_location']}")


if __name__ == '__main__':
    main()
