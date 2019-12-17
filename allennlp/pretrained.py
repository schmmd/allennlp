import warnings

from allennlp import predictors
from allennlp.predictors import Predictor
from allennlp.models.archival import load_archive


class PretrainedModel:
    """
    A pretrained model is determined by both an archive file
    (representing the trained model)
    and a choice of predictor.
    """

    def __init__(self, archive_file: str, predictor_name: str) -> None:
        self.archive_file = archive_file
        self.predictor_name = predictor_name

    def predictor(self) -> Predictor:
        archive = load_archive(self.archive_file)
        return Predictor.from_archive(archive, self.predictor_name)


# TODO(Mark): Figure out a way to make PretrainedModel generic on Predictor, so we can remove these type ignores.

# Models in the demo


def srl_with_elmo_luheng_2018() -> predictors.SemanticRoleLabelerPredictor:
    """
    Semantic Role Labeling

    Based on [He et al, 2017](https://www.semanticscholar.org/paper/Deep-Semantic-Role-Labeling-What-Works-and-What-s-He-Lee/a3ccff7ad63c2805078b34b8514fa9eab80d38e9)

    f1: 0.849
    """
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://allennlp.s3.amazonaws.com/models/srl-model-2018.05.25.tar.gz",
            "semantic-role-labeling",
        )
        return model.predictor()  # type: ignore


def bert_srl_shi_2019() -> predictors.SemanticRoleLabelerPredictor:
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://s3-us-west-2.amazonaws.com/allennlp/models/bert-base-srl-2019.06.17.tar.gz",
            "semantic-role-labeling",
        )
        return model.predictor()  # type: ignore


def bidirectional_attention_flow_seo_2017() -> predictors.BidafPredictor:
    """
    Reading Comprehension

    Based on `BiDAF (Seo et al, 2017) <https://www.semanticscholar.org/paper/Bidirectional-Attention-Flow-for-Machine-Comprehen-Seo-Kembhavi/007ab5528b3bd310a80d553cccad4b78dc496b02>`_

    .. code-block:: bash

       $ docker run allennlp/allennlp:v0.7.0
           evaluate
           https://allennlp.s3.amazonaws.com/models/bidaf-model-2017.09.15-charpad.tar.gz
           https://allennlp.s3.amazonaws.com/datasets/squad/squad-dev-v1.1.json

    Metrics:

    * start_acc: 0.642
    * end_acc: 0.671
    * span_acc: 0.552
    * em: 0.683
    * f1: 0.778
    """
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://allennlp.s3.amazonaws.com/models/bidaf-model-2017.09.15-charpad.tar.gz",
            "machine-comprehension",
        )
        return model.predictor()  # type: ignore


def naqanet_dua_2019() -> predictors.BidafPredictor:
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://allennlp.s3.amazonaws.com/models/naqanet-2019.04.29-fixed-weight-names.tar.gz",
            "machine-comprehension",
        )
        return model.predictor()  # type: ignore


def open_information_extraction_stanovsky_2018() -> predictors.OpenIePredictor:
    model = PretrainedModel(
        "https://allennlp.s3.amazonaws.com/models/openie-model.2018-08-20.tar.gz",
        "open-information-extraction",
    )
    return model.predictor()  # type: ignore


def decomposable_attention_with_elmo_parikh_2017() -> predictors.DecomposableAttentionPredictor:
    """
    Textual Entailment

    Based on `Parikh et al, 2017 <https://www.semanticscholar.org/paper/A-Decomposable-Attention-Model-for-Natural-Languag-Parikh-T%C3%A4ckstr%C3%B6m/07a9478e87a8304fc3267fa16e83e9f3bbd98b27>`_

    .. code-block:: bash

       $ docker run allennlp/allennlp:v0.7.0
           evaluate
           https://allennlp.s3.amazonaws.com/models/decomposable-attention-elmo-2018.02.19.tar.gz
           https://allennlp.s3.amazonaws.com/datasets/snli/snli_1.0_test.jsonl

    Metrics:
    accuracy: 0.864
    """
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://allennlp.s3.amazonaws.com/models/decomposable-attention-elmo-2018.02.19.tar.gz",
            "textual-entailment",
        )
        return model.predictor()  # type: ignore


def neural_coreference_resolution_lee_2017() -> predictors.CorefPredictor:
    """
    Coreference Resolution

    Based on `End-to-End Coreference Resolution (Lee et al, 2017) <https://www.semanticscholar.org/paper/End-to-end-Neural-Coreference-Resolution-Lee-He/3f2114893dc44eacac951f148fbff142ca200e83>`_

    f1: 0.630
    """
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://allennlp.s3.amazonaws.com/models/coref-model-2018.02.05.tar.gz",
            "coreference-resolution",
        )
        predictor = model.predictor()

        predictor._dataset_reader._token_indexers[  # type: ignore
            "token_characters"
        ]._min_padding_length = 5
        return predictor  # type: ignore


def named_entity_recognition_with_elmo_peters_2018() -> predictors.SentenceTaggerPredictor:
    """
    Named Entity Recognition

    Based on `Deep contextualized word representations <https://arxiv.org/abs/1802.05365>`_
    """
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://allennlp.s3.amazonaws.com/models/ner-model-2018.12.18.tar.gz",
            "sentence-tagger",
        )
        predictor = model.predictor()

        predictor._dataset_reader._token_indexers[  # type: ignore
            "token_characters"
        ]._min_padding_length = 3
        return predictor  # type: ignore


def fine_grained_named_entity_recognition_with_elmo_peters_2018() -> predictors.SentenceTaggerPredictor:
    """
    Fine Grained Named Entity Recognition
    """
    model = PretrainedModel(
        "https://allennlp.s3.amazonaws.com/models/fine-grained-ner-model-elmo-2018.12.21.tar.gz",
        "sentence-tagger",
    )
    predictor = model.predictor()

    predictor._dataset_reader._token_indexers[  # type: ignore
        "token_characters"
    ]._min_padding_length = 3
    return predictor  # type: ignore


def span_based_constituency_parsing_with_elmo_joshi_2018() -> predictors.ConstituencyParserPredictor:
    """
    Constituency Parsing

    Based on `Minimal Span Based Constituency Parser (Stern et al, 2017) <https://www.semanticscholar.org/paper/A-Minimal-Span-Based-Neural-Constituency-Parser-Stern-Andreas/593e4e749bd2dbcaf8dc25298d830b41d435e435>`_ but with ELMo embeddings
    """
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://allennlp.s3.amazonaws.com/models/elmo-constituency-parser-2018.03.14.tar.gz",
            "constituency-parser",
        )
        return model.predictor()  # type: ignore


def biaffine_parser_stanford_dependencies_todzat_2017() -> predictors.BiaffineDependencyParserPredictor:
    """
    Biaffine Dependency Parser

    Based on `Dozat and Manning, 2017 <https://arxiv.org/pdf/1611.01734.pdf>`_
    """
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://allennlp.s3.amazonaws.com/models/biaffine-dependency-parser-ptb-2018.08.23.tar.gz",
            "biaffine-dependency-parser",
        )
        return model.predictor()  # type: ignore


# Models not in the demo

"""
Biaffine Dependency Parser

Based on [Dozat and Manning, 2017](https://arxiv.org/pdf/1611.01734.pdf)
"""


def biaffine_parser_universal_dependencies_todzat_2017() -> predictors.BiaffineDependencyParserPredictor:
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://allennlp.s3.amazonaws.com/models/biaffine-dependency-parser-ud-2018.08.23.tar.gz",
            "biaffine-dependency-parser",
        )
        return model.predictor()  # type: ignore


def esim_nli_with_elmo_chen_2017() -> predictors.DecomposableAttentionPredictor:
    """
    ESIM

    Based on `Enhanced LSTM for Natural Language Inference <https://arxiv.org/pdf/1609.06038.pdf>`_ and uses ELMo
    """
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=DeprecationWarning)
        model = PretrainedModel(
            "https://allennlp.s3.amazonaws.com/models/esim-elmo-2018.05.17.tar.gz",
            "textual-entailment",
        )
        return model.predictor()  # type: ignore
