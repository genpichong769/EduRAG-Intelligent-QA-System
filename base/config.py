import ast
import configparser
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    # python-dotenv is included in the project requirements. Keeping this
    # optional lets configuration-only tooling run before dependencies install.
    pass


class Config:
    """Load local configuration without embedding credentials in source code."""

    def __init__(self, config_file=None):
        configured_path = config_file or os.getenv("EDURAG_CONFIG_FILE")
        self.config_file = Path(configured_path) if configured_path else PROJECT_ROOT / "config.ini"

        self.config = configparser.ConfigParser()
        self.config.read(self.config_file, encoding="utf-8")

        # Environment variables take precedence over config.ini.
        self.MYSQL_HOST = self._get("MYSQL_HOST", "mysql", "host", "localhost")
        self.MYSQL_USER = self._get("MYSQL_USER", "mysql", "user", "root")
        self.MYSQL_PASSWORD = self._get("MYSQL_PASSWORD", "mysql", "password", "")
        self.MYSQL_DATABASE = self._get("MYSQL_DATABASE", "mysql", "database", "subjects_kg")

        self.REDIS_HOST = self._get("REDIS_HOST", "redis", "host", "localhost")
        self.REDIS_PORT = int(self._get("REDIS_PORT", "redis", "port", "6379"))
        self.REDIS_PASSWORD = self._get("REDIS_PASSWORD", "redis", "password", "") or None
        self.REDIS_DB = int(self._get("REDIS_DB", "redis", "db", "0"))

        self.MILVUS_HOST = self._get("MILVUS_HOST", "milvus", "host", "localhost")
        self.MILVUS_PORT = self._get("MILVUS_PORT", "milvus", "port", "19530")
        self.MILVUS_DATABASE_NAME = self._get(
            "MILVUS_DATABASE_NAME", "milvus", "database_name", "itcast"
        )
        self.MILVUS_COLLECTION_NAME = self._get(
            "MILVUS_COLLECTION_NAME", "milvus", "collection_name", "edurag_final"
        )

        # DashScope exposes an OpenAI-compatible API. API_KEY is kept for
        # backwards compatibility with existing local environments.
        self.LLM_MODEL = self._get("LLM_MODEL", "llm", "model", "qwen-plus")
        self.DASHSCOPE_API_KEY = (
            os.getenv("DASHSCOPE_API_KEY")
            or os.getenv("API_KEY")
            or self.config.get("llm", "dashscope_api_key", fallback="")
        )
        self.DASHSCOPE_BASE_URL = self._get(
            "DASHSCOPE_BASE_URL",
            "llm",
            "dashscope_base_url",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        self.PARENT_CHUNK_SIZE = int(
            self._get("PARENT_CHUNK_SIZE", "retrieval", "parent_chunk_size", "1200")
        )
        self.CHILD_CHUNK_SIZE = int(
            self._get("CHILD_CHUNK_SIZE", "retrieval", "child_chunk_size", "300")
        )
        self.CHUNK_OVERLAP = int(
            self._get("CHUNK_OVERLAP", "retrieval", "chunk_overlap", "50")
        )
        self.RETRIEVAL_K = int(self._get("RETRIEVAL_K", "retrieval", "retrieval_k", "5"))
        self.CANDIDATE_M = int(self._get("CANDIDATE_M", "retrieval", "candidate_m", "2"))

        sources = self._get(
            "VALID_SOURCES", "app", "valid_sources", '["ai", "java", "test", "ops", "bigdata"]'
        )
        self.VALID_SOURCES = ast.literal_eval(sources)
        self.CUSTOMER_SERVICE_PHONE = self._get(
            "CUSTOMER_SERVICE_PHONE", "app", "customer_service_phone", "your_phone_here"
        )
        self.LOG_FILE = self._get("LOG_FILE", "logger", "log_file", "logs/app.log")

        # Local model artifacts are intentionally excluded from Git.
        self.bge_m3 = os.getenv(
            "BGE_M3_PATH", str(PROJECT_ROOT / "rag_qa" / "models" / "bge-m3")
        )
        self.bge_reranker = os.getenv(
            "BGE_RERANKER_PATH",
            str(PROJECT_ROOT / "rag_qa" / "models" / "bge-reranker-large"),
        )
        self.nlp_bert_doc_seg = os.getenv(
            "DOCUMENT_SEGMENTATION_MODEL_PATH",
            str(PROJECT_ROOT / "rag_qa" / "models" / "nlp_bert_document-segmentation_chinese-base"),
        )
        self.bert_intent_cls = os.getenv(
            "QUERY_CLASSIFIER_MODEL_PATH",
            str(PROJECT_ROOT / "rag_qa" / "core" / "bert_query_classifier"),
        )

    def _get(self, env_name, section, option, fallback):
        value = os.getenv(env_name)
        if value is not None:
            return value
        return self.config.get(section, option, fallback=fallback)


if __name__ == "__main__":
    conf = Config()
    print(conf.MYSQL_HOST)
