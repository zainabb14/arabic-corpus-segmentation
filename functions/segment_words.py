from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer


def camel_segment(text):
    mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
    msa_bw_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='bwtok')
    msa_bw_tok = msa_bw_tokenizer.tokenize(text)
    return msa_bw_tok