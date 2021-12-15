from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from datasets import Dataset
from collections import defaultdict
from transformers import Trainer, TrainingArguments, EarlyStoppingCallback
import torch
import argparse

torch.manual_seed(0)


def get_raw_data(data_location: str):
    data = defaultdict(list)
    with open(data_location, "r") as data_file:
        for line in data_file:
            prose, poetry = line.split('\t')
            data['prose'].append(prose)
            data['poetry'].append(poetry)
    return Dataset.from_dict(data)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_size", type=float, default=0.9)
    parser.add_argument("--max_sentence_length", type=int, default=150)
    parser.add_argument("--model_name", type=str, default="sberbank-ai/ruT5-base")
    parser.add_argument("--checkpoint_location", type=str)
    parser.add_argument("--data_location", type=str)
    parser.add_argument("--epoch_counts", type=int, default=10)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=8)
    parser.add_argument("--per_device_train_batch_size", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=1e-4)
    parser.add_argument("--per_device_eval_batch_size", type=int, default=16)
    return parser.parse_args()


def tokenize_function(examples, tokenizer, max_length: int):
    result = tokenizer(examples["prose"], padding='max_length',
                       max_length=max_length, truncation=True)
    labels = tokenizer(examples['poetry'], padding='max_length',
                       max_length=max_length, truncation=True,
                       return_attention_mask=False).input_ids
    result['labels'] = [
           [(label if label != tokenizer.pad_token_id else -100) for label in labels_example] for labels_example in labels
    ]
    return result


def get_tokenizer(model_name: str, checkpoint_location: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.add_tokens("\n")
    tokenizer.save_pretrained(checkpoint_location)
    return tokenizer


def get_tokenized_data(raw_dataset, model_name: str, checkpoint_location: str, max_size: int):
    tokenizer = get_tokenizer(model_name, checkpoint_location)
    return raw_dataset.map(lambda x: tokenize_function(x, tokenizer, max_size), batched=True)


def get_data(data_location: str, train_size: float, model_name: str, checkpoint_location: str, max_size: int):
    raw_data = get_raw_data(data_location)
    tokenized_data = get_tokenized_data(raw_data, model_name, checkpoint_location, max_size).train_test_split(train_size=train_size)
    return tokenized_data['train'], tokenized_data['test']


def train_model(args):
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model_name)
    train_data, val_data = get_data(args.data_location, args.train_size, args.model_name,
                                    args.checkpoint_location, args.max_sentence_length)
    print(train_data, val_data)
    training_arguments = TrainingArguments(output_dir=args.checkpoint_location, do_train=True,
                                           do_eval=True, overwrite_output_dir=True,
                                           evaluation_strategy="steps", eval_steps=10000,
                                           per_device_train_batch_size=args.per_device_train_batch_size,
                                           gradient_accumulation_steps=args.gradient_accumulation_steps,
                                           learning_rate=args.learning_rate, save_strategy="steps", save_steps=10000,
                                           per_device_eval_batch_size=args.per_device_eval_batch_size,
                                           num_train_epochs=args.epoch_counts, load_best_model_at_end=True)
    trainer = Trainer(model=model, args=training_arguments,
                      train_dataset=train_data, eval_dataset=val_data,
                      callbacks=[EarlyStoppingCallback(early_stopping_patience=3)])
    trainer.train()


if __name__ == '__main__':
    args = parse_args()
    train_model(args)
