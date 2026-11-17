
import os
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer


class ONNXEmbeddingEngine:

    def __init__(self):
        model_dir = os.path.join(
            os.path.dirname(__file__),
            "onnx_model"
        )

        model_path = os.path.join(
            model_dir,
            "model_quantized.onnx"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_dir,
            local_files_only=True
        )

        options = ort.SessionOptions()
        options.intra_op_num_threads = 1
        options.inter_op_num_threads = 1

        self.session = ort.InferenceSession(
            model_path,
            sess_options=options,
            providers=["CPUExecutionProvider"]
        )

    def encode(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        tokens = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="np"
        )

        inputs = {
            item.name: tokens[item.name]
            for item in self.session.get_inputs()
        }

        outputs = self.session.run(None, inputs)
        token_embeddings = outputs[0]

        mask = tokens["attention_mask"][:, :, None].astype(
            np.float32
        )

        embeddings = (
            (token_embeddings * mask).sum(axis=1)
            / np.maximum(mask.sum(axis=1), 1e-9)
        )

        norms = np.linalg.norm(
            embeddings,
            axis=1,
            keepdims=True
        )

        embeddings = embeddings / np.maximum(norms, 1e-12)

        return embeddings


engine = ONNXEmbeddingEngine()
