# Model Fine Tuning
To fine tune model from Huggingface use script:
```bash
python train.py --train_size 0.9 --max_sentence_length 150 \\
                   --model_name "sberbank-ai/ruT5-base" \\
                   --checkpoint_location PLACE_TO_SAVE \\
                   --data_location PATH_TO_DATA \\
                   --epoch_counts TRAIN_EPOCHUES_COUNT \\
                   --gradient_accumulation_steps 4 \\
                   --per_device_train_batch_size 8 \\
                   --learning_rate 1e-4 \\
                   --per_device_eval_batch_size 16
```
Change `--model_name` for different pretrained models. `--gradient_accumulation_steps` and `--per_device_train_batch_size`
are selected so that we can use batch of size 32 for training on 16Gb GPU memory.
