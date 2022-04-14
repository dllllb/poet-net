from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List

class PoetryGenerator:
    """
    Generates new rhyming data based on initial prosaic text
    
    Attributes
    ----------
    model : transformers ModelForSeq2SeqLM used for initial candidate generation
    tokenizer : corresponden to model tokenizer
    rhyme_tagger : RhymeTagger form rhymetagger package used for detecting
    rhyming phrases https://github.com/versotym/rhymetagger
    cuda_id : str cuda device CPU or CUDA:i
    max_len : int max len of the sentenses
    candidates_count : int max number of rhyming candidates

    Methods
    -------
    generate_rhymes(phrase: str) -> List[str] : Generate rhymes based on input phrase
    """

    def __init__(self, model: AutoModelForSeq2SeqLM, tokenizer: AutoTokenizer, rhyme_tagger: RhymeTagger, cuda_id: str, max_len: int = 50, candidates_count: int = 150):
        self.model = model
        self.tokenizer = tokenizer
        self.rhyme_tagger = rhyme_tagger
        self.cuda_id = cuda_id
        self.max_len = max_len
        self.candidates_count = candidates_count

    def __generate_new_texts(self, phrase: str, candidate_counts=150) -> List[str]:
        tokens = self.tokenizer(phrase, return_tensors='pt').input_ids.to(self.cuda_id)
        if len(tokens) > self.max_len:
            return None
        generation_output = self.model.generate(tokens, return_dict_in_generate=False,
            num_beams=candidate_counts,
            num_return_sequences=candidate_counts,max_length=self.max_len)
        decoded_texts = self.tokenizer.batch_decode(generation_output,skip_special_tokens=True)
        return [elem.replace("\n ", "\\n") for elem in decoded_texts]

    def __is_rhyming(self, phrase: List[str]) -> bool:
        rhymes = self.rhyme_tagger.tag(phrase.split("\\n"), output_format=3)
        return None not in rhymes

    def generate_rhymes(self, phrase: str) -> List[str]:
        candidates = self.__generate_new_texts(phrase, self.candidates_count)
        if candidates is None:
            return None
        return [(new_phrase, index) for index, new_phrase in enumerate(candidates) if self.__is_rhyming(new_phrase)]