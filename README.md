# poet-net

## Models

- [MT5 model](https://huggingface.co/dllllb/poetnet-mt5-stihiru-libru), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/di-datasets/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/di-datasets/libru-poetry.zip) dataset
- [RUT5 model](https://huggingface.co/dllllb/poetnet-rut5-stihiru-libru), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/di-datasets/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/di-datasets/libru-poetry.zip) dataset
- [RUT5 model](https://huggingface.co/dllllb/poetnet-rut5-stihiru-libru-finetune), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/di-datasets/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/di-datasets/libru-poetry.zip) dataset, and then additionaly fine-tuned on the Taiga Fontanka headers dataset, where the rhythmed pair was produced by the previous version of the model
