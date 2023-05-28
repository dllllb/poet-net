# poet-net

## Models

- [MT5 model](https://huggingface.co/dllllb/poetnet-mt5-stihiru-libru), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/poet-net/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/poet-net/libru-poetry.zip) dataset
- [RUT5 model](https://huggingface.co/dllllb/poetnet-rut5-stihiru-libru) (RUT5-1), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/poet-net/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/poet-net/libru-poetry.zip) dataset
- [RUT5 model](https://huggingface.co/dllllb/poetnet-rut5-stihiru-libru-finetune) (RUT5-2), trained on [Taiga stihi.ru](https://storage.yandexcloud.net/poet-net/taiga-stihi-ru.zip) dataset and [Lib.ru poetry](https://storage.yandexcloud.net/poet-net/libru-poetry.zip) dataset, and then additionaly fine-tuned on the Taiga Fontanka headers dataset, where the rhythmed pair was produced by the previous version of the model

## Overview of the approach

The paired dataset of rhymed and not rhymed text is required to train a Seq2Seq model to transfrom plain text the poetry. We synthetically generate paired dataset from rhymed text dataset using machine translation. Machine translation allows to obtain plain text by tranlsating a poem to some foreign language and then back to the original language (back-translation). This approach will produce wo versions of the same text, the mangled automatiaclly translated plain version and the original poetic version.

The text styling net outputs can be ranked using additional discriminator net, trained on the unpaired dataset of both rhymed and not rhymed texts. It is also possilbe to fine-tune text styling net by selecting highly ranked outputs and add them to the training set.

The same approach can be used for any style transfer task where a substantial volume of styled text is available.

## RUT5-1 output

"Это не единственная погодная неприятность, которая нас ждет."

51
Вот такая непогода 
Не одна у нас беда.

72
Вот такая непогода 
Ждёт нас не одна беда.

"Курьер опаздает из-за большой пробки на садовом"

52
Курьер опаздает из-за большой 
пробки на садовой

248
Курьер опаздает из-за большой 
Пробки на садовой

"Он всегда пытался руководствоваться принципом: Пришел, увидел, победил"

31
Он принципом всегда водил: 
Пришел, увидел, победил

59
Он принципом всегда движим был: 
Пришел, увидел, победил

63
Он принципом всегда движим был: 
Пришёл, увидел, победил

69
Он принципом всегда водил: 
Пришёл, увидел, победил

102
Он движим принципом всегда был: 
Пришёл, увидел, победил

111
Он движим принципом всегда был: 
Пришел, увидел, победил

## Related papers

The back-translation paraphrasing approach is proposed in the Paraphrasing with Bilingual Parallel Corpora / Bannard & Callison-Burch / ACL 2005
