# poet-net

## Models

- [MT5 model](https://storage.yandexcloud.net/di-models/poetnet-mt5-taiga-libru.bin), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/di-datasets/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/di-datasets/libru-poetry.zip) dataset
- [RUT5 model](https://storage.yandexcloud.net/di-models/poetnet-rutp5-taiga-libru.bin), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/di-datasets/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/di-datasets/libru-poetry.zip) dataset
- [RUT5 model](https://storage.yandexcloud.net/di-models/poetnet-rutp5-taiga-libru-finetune.bin), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/di-datasets/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/di-datasets/libru-poetry.zip) dataset, and then additionaly fine-tuned on the Taiga Fontanka headers dataset, where the rhythmed pair was produced by the previous version of the model
