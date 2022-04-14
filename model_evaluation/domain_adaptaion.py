from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from PoetryGenerator import PoetryGenerator
from typing import List
from rhymetagger import RhymeTagger
from tqdm import tqdm
import sys

CUDA_ID = sys.argv[1]
MODEL_LOCATION = "/mnt/smolyakov/rutp5_update/checkpoint-20664/"
MODEL_NAME = "sberbank-ai/ruT5-large"
NEW_DATASET_LOCATION = f"/mnt/smolyakov/new_data_block_with_counter_{CUDA_ID}.txt"
OLD_DATA = "/mnt/smolyakov/fontantka_headlines.txt"


def get_rhyme_tagger() -> RhymeTagger:
    rt = RhymeTagger()
    rt.load_model(model='ru')
    return rt


def get_rhyme_generator() -> PoetryGenerator:
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_LOCATION).to(f"cuda:{CUDA_ID}")
    print("Load model")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    print("Load tokenizer")
    tokenizer.add_tokens("\n")
    rhyme_tagger = get_rhyme_tagger()
    return PoetryGenerator(model, tokenizer, rhyme_tagger, "CUDA:0")


def save_block(text:str, all_targets: List[str], file_location: str) -> None:
    with open(file_location, "a") as data_file:
        for index, target in all_targets:
            data_file.write(f"{text}\t{target}\t{index}\n")


def get_data():
    with open(OLD_DATA, 'r') as data_file:
        data = data.readlines()
    cuda_int = int(CUDA_ID)
    return data[len(data)//4 * cuda_int: len(data) // 4 * (cuda_int + 1)]


def get_phrases() -> List[str]:
    with open(OLD_DATA, "r") as data_file:
        data = data_file.read().split("\n")
        cuda_int = int(CUDA_ID)
        return data[len(data)//4 * cuda_int: len(data) // 4 * (cuda_int + 1)]

def main():
    all_phrases = get_phrases()
    print("Load phrases")
    rhyme_generator = get_rhyme_generator()
    print(rhyme_generator)
    print("Get Rhyme Generator")
    for phrase in tqdm(all_phrases):
        rhymes = rhyme_generator.generate_rhymes(phrase)
        if rhymes is not None:
            save_block(phrase, rhymes, NEW_DATASET_LOCATION)
        else:
            save_block(phrase, [(-1, "")], NEW_DATASET_LOCATION)


if __name__ == "__main__":
    main()
