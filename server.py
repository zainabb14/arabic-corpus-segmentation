import unicodedata
from flask import Flask, render_template, request
from functions import handle_upload_file, handle_extract_words, pyaramorph_segment, analyze_segmentation, \
    get_affixes,get_root,is_arabic
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, unique=True)
    root = db.Column(db.String)
    camel_segmented = db.Column(db.String)
    pyaramorph_segmented = db.Column(db.String)
    camel_prefix = db.Column(db.String)
    camel_suffix = db.Column(db.String)
    camel_stem = db.Column(db.String)
    pyaramorph_prefix = db.Column(db.String)
    pyaramorph_suffix = db.Column(db.String)
    pyaramorph_stem = db.Column(db.String)
    camel_confidence = db.Column(db.Integer, nullable=True)
    pyaramorph_confidence = db.Column(db.Integer, nullable=True)
    same_flag = db.Column(db.Integer, nullable=True)

from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer

valid_prefixes = ['ال', 'ب', 'ك', 'ل', 'و', 'س', 'ف', 'ت', 'أ']
valid_suffixes = ['ه', 'ها', 'ك', 'ي', 'نا', 'كم', 'كن', 'هم', 'هن', 'ت', 'ون', 'ين', 'ات', 'ة']

def camel_segment1(text,msa_bw_tokenizer):
    msa_bw_tok = msa_bw_tokenizer.tokenize(text)
    return msa_bw_tok

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        uploaded_file = request.files['file']
        file = handle_upload_file(uploaded_file)
        text = handle_extract_words(file)
        segmentation_results = []

        mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
        msa_bw_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='bwtok')

        pyaramorph_segmentations = pyaramorph_segment(text)
        camel_segmentations = [' '.join(camel_segment1([word],msa_bw_tokenizer)).replace("+_", " ").replace("_+", " ") for word in text]


        for i, word in enumerate(text):
            camel_segmentation = camel_segmentations[i]
            pyaramorph_segmentation = pyaramorph_segmentations[i]
            camel_affixes = get_affixes(camel_segmentation)
            pyaramorph_affixes = get_affixes(pyaramorph_segmentation)

            root = get_root(word)

            same_flag = None
            camel_confidence = None
            pyaramorph_confidence = None

            if unicodedata.normalize('NFC', camel_segmentation) == unicodedata.normalize('NFC',
                                                                                         pyaramorph_segmentation):
                same_flag = 1
            else:
                camel_confidence, pyaramorph_confidence = analyze_segmentation(
                    camel_segmentation=camel_segmentation,
                    pyaramorph_segmentation=pyaramorph_segmentation
                )

            if not is_arabic(pyaramorph_segmentation):
                pyaramorph_segmentation = None
                pyaramorph_affixes = {"prefixes": None, "suffixes": None, "stem": None}

            if "suffixes" in camel_affixes:
                camel_affixes["suffixes"] = [suffix for suffix in camel_affixes["suffixes"] if suffix in valid_suffixes]
            else:
                camel_affixes["suffixes"] = None

            if pyaramorph_affixes["prefixes"] is not None:
                pyaramorph_affixes["prefixes"] = [prefix for prefix in pyaramorph_affixes["prefixes"] if prefix in valid_prefixes]
            else:
                pyaramorph_affixes["prefixes"] = None

            if pyaramorph_affixes["suffixes"] is not None:
                pyaramorph_affixes["suffixes"] = [suffix for suffix in pyaramorph_affixes["suffixes"] if suffix in valid_suffixes]
            else:
                pyaramorph_affixes["suffixes"] = None

            segmentation_results.append({
                "word": word,
                "root":root,
                "camel_segmented": camel_segmentation,
                "pyaramorph_segmented": pyaramorph_segmentation,
                "camel_confidence": camel_confidence,
                "pyaramorph_confidence": pyaramorph_confidence,
                "same_flag": same_flag
            })
            existing_word = Words.query.filter_by(word=word).first()
            if not existing_word:
                new_word = Words(
                    word=word,
                    root=root,
                    camel_segmented=camel_segmentation,
                    pyaramorph_segmented=pyaramorph_segmentation,
                    camel_prefix=str(camel_affixes["prefixes"]),
                    camel_suffix=str(camel_affixes["suffixes"]),
                    camel_stem=str(camel_affixes["stem"]),
                    pyaramorph_prefix=str(pyaramorph_affixes["prefixes"]),
                    pyaramorph_suffix=str(pyaramorph_affixes["suffixes"]),
                    pyaramorph_stem=str(pyaramorph_affixes["stem"]),
                    camel_confidence=camel_confidence,
                    pyaramorph_confidence=pyaramorph_confidence,
                    same_flag=same_flag
                )
                db.session.add(new_word)
            print(f'Word {i} of {len(text)} is Done')
        db.session.commit()
        return render_template('result.html', results=segmentation_results)


if __name__ == '__main__':
    app.run(debug=True)