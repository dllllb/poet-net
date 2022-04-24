from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from PoetryGenerator import PoetryGenerator
from typing import List
from rhymetagger import RhymeTagger
import argparse
from tqdm import tqdm
import sys


def get_rhyme_tagger() -> RhymeTagger:
    rt = RhymeTagger()
    rt.load_model(model='ru')
    return rt


def get_rhyme_generator(args) -> PoetryGenerator:
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model_name).to(args.cuda_device)
    print("Load model")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    print("Load tokenizer")
    rhyme_tagger = get_rhyme_tagger()
    return PoetryGenerator(model, tokenizer, rhyme_tagger, args.cuda_device)


def save_block(text:str, all_targets: List[str], file_location: str) -> None:
    with open(file_location, "a") as data_file:
        for index, target in all_targets:
            data_file.write(f"{text}\t{target}\t{index}\n")


def get_data(args):
    with open(args.data_location, 'r') as data_file:
        data = data_file.readlines()
    return data


def get_phrases(args) -> List[str]:
    with open(args.data_location, "r") as data_file:
        data = data_file.read().split("\n")
    return data


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cuda_device", type=str, default='cpu')
    parser.add_argument("--model_name", type=str, default="dllllb/poetnet-rut5-stihiru-libru")
    parser.add_argument("--data_location", type=str, default="data/fontantka_headlines.txt")
    parser.add_argument("--new_data_location", type=str, default="data/new_data.txt")
    return parser.parse_args()


def main(args):
    all_phrases = get_phrases(args)
    print("Load phrases")
    rhyme_generator = get_rhyme_generator(args)
    print(rhyme_generator)
    print("Get Rhyme Generator")
    for phrase in tqdm(all_phrases):
        rhymes = rhyme_generator.generate_rhymes(phrase)
        if rhymes is not None:
            save_block(phrase, rhymes, args.new_data_location)
        else:
            save_block(phrase, [(-1, "")], args.new_data_location)


if __name__ == "__main__":
    args = parse_args()
    main(args)
