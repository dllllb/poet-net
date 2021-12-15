## Dataset Preparation

### Raw data Source
There are two sources of raw data in this project:
* Poetry from www.lib.ru
* Poetry from [Taiga Corpus](https://tatianashavrina.github.io/taiga_site/)

#### lib.ru crawler

To crawl raw data from lib.ru:
```bash
python libru_crawler.py LOCATION_TO_SAVE
```
Data will be saved as json with schema
```
[(author_id, [(book_id, [texts])])];
```

#### Taiga ru preparation
For some reasons block with texts from stihi.ru is not accessible for direct download. And archive https://linghub.ru/static/Taiga/stihi_ru.zip
is broken. So we have to download the whole dataset (untagged part) and take poetry data.

WARNING untagged dataset version requires 15Gb disk space. By default data will be downloading into current directory
```bash
bash download_taiga_ru_poetry.sh
python taiga_ru_json_generation.py ./stihi_ru/texts stih_ru.json
rm -r stihi_ru/
```

### Splitting Into Rhyming Groups
We split raw data into separate groups based on rhyming properties. We used [RhymeTagger](https://github.com/versotym/rhymetagger) to detect rhyming lines and
separate them.

To split data from JSON file prepared on previous step:
```bash
python text_splitter.py --json_data_location PATH_TO_DATA_FROM_PREVIOUS_STEP --splitted_dataset_location NEW_DATA_LOCATION
```

### Generating Parallel Corpus
We translate blocks from previous steps to english and back to russian to keep content but remove stylistic properties.

Translation was made with [WMT19 News Translation Task](https://arxiv.org/abs/1907.06616)

To generate parallel dataset:
```bash
python create_parallel_corpus.py --prose_poetry_file_location --poetry_data_location --device  --batch_size --ru_en_model --en_ru_model
```