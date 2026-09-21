# Knowledge-base data

本目录用于存放本地知识库原文。原始课程资料可能包含私有或受版权保护的内容，因此不进入 Git。

系统当前支持 `txt`、`md`、`pdf`、`docx`、`ppt`、`pptx`、`jpg`、`png`。建议按 `<source>_data` 命名子目录，例如 `ai_data`；目录名会转换为 Milvus 中的 `source` 元数据。

准备数据后，可调用 `rag_qa.core.document_processor.process_documents` 完成父子分块，再通过 `rag_qa.core.vector_store.VectorStore.add_documents` 写入 Milvus。完整示例见项目根目录 README。
