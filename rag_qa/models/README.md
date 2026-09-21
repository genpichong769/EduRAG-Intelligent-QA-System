# Local model artifacts

模型权重不进入 Git。运行完整检索链路前，请准备以下目录：

```text
rag_qa/models/
├── bge-m3/
├── bge-reranker-large/
└── nlp_bert_document-segmentation_chinese-base/  # 仅语义切分实验需要
```

`BAAI/bge-m3` 与 `BAAI/bge-reranker-large` 可通过 Hugging Face Hub 下载。路径也可分别用 `BGE_M3_PATH`、`BGE_RERANKER_PATH` 覆盖。

查询分类器是项目训练产物，默认放在 `rag_qa/core/bert_query_classifier/`；该目录同样被忽略，可用 `QUERY_CLASSIFIER_MODEL_PATH` 指向其他本地目录。
