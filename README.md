# poet-net

## Models

- [MT5 model](https://huggingface.co/dllllb/poetnet-mt5-stihiru-libru), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/di-datasets/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/di-datasets/libru-poetry.zip) dataset
- [RUT5 model](https://huggingface.co/dllllb/poetnet-rut5-stihiru-libru), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/di-datasets/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/di-datasets/libru-poetry.zip) dataset
- [RUT5 model](https://huggingface.co/dllllb/poetnet-rut5-stihiru-libru-finetune), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/di-datasets/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/di-datasets/libru-poetry.zip) dataset, and then additionaly fine-tuned on the Taiga Fontanka headers dataset, where the rhythmed pair was produced by the previous version of the model

## Overview of the approach

The paired dataset of rhymed and not rhymed text is required to train a Seq2Seq model to transfrom plain text the poetry. We synthetically generate paired dataset from rhymed text dataset using machine translation. Machine translation allows to obtain plain text by tranlsating a poem to some foreign language and then back to the original language (back-translation). This approach will produce wo versions of the same text, the mangled automatiaclly translated plain version and the original poetic version.

The text styling net outputs can be ranked using additional discriminator net, trained on the unpaired dataset of both rhymed and not rhymed texts. It is also possilbe to fine-tune text styling net by selecting highly ranked outputs and add them to the training set.

The same approach can be used for any style transfer task where a substantial volume of styled text is available.

## Related papers

Russian Paraphrasers: Paraphrase with Transformers / Alena Fenogenova / BSNLP 2021
