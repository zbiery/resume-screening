import os
import asyncio
from abc import ABC
from collections.abc import AsyncGenerator
from typing import IO, List

from pypdf import PdfReader
from docx import Document

from ..common.logger import get_logger

logger = get_logger(__name__)

class Parser(ABC):
    """
    Abstract parser that parses content into text
    """
    async def parse(self, content: IO) -> AsyncGenerator[str, None]:
        if False:
            yield  # pragma: no cover - this is necessary for mypy to type check

class PdfParser(Parser):
    "Concrete parser for pdf documents"

    async def parse(self, content: IO) -> AsyncGenerator[str, None]:
        logger.info("Extracting text from '%s' using local PDF parser (pypdf)", content.name)

        reader = PdfReader(content)
        pages = reader.pages
        for p in pages:
            text = p.extract_text()
            if text:
                yield text

class DocxParser(Parser):
    "Concrete parser for docx documents"

    async def parse(self, content: IO) -> AsyncGenerator[str, None]:
        logger.info("Extracting text from '%s' using local Docx parser (python-docx)", content.name)
        
        reader = Document(content)
        paragraphs = reader.paragraphs

        for para in paragraphs:
            text = para.text.strip()
            if text:
                yield text

class FileProcessor():
    """
    Processes a resume file and delegates parsing to the appropriate parser
    based on file extension.
    """

    def __init__(self):
        self.parsers = {
            ".pdf": PdfParser(),
            ".docx": DocxParser(),
        }

    async def process(self, content: IO) -> List[str]:
        "Method for extracting text from content objects"
        _, ext = os.path.splitext(content.name.lower())

        parser = self.parsers.get(ext)
        if not parser:
            logger.error("Unsupported file extension: %s", ext)
            raise ValueError(f"Unsupported file extension: {ext}")

        logger.info("Using %s parser for file: %s", ext.upper(), content.name)
        return [chunk async for chunk in parser.parse(content)]

    async def extract_from_file(self, file_path: str) -> str:
        """
        Extracts and returns all text from a local file path as a single string.
        """
        logger.info("Extracting text from local file: %s", file_path)
        text_chunks = []

        with open(file_path, "rb") as f:
            chunks = await self.process(f)

        return "\n".join(chunk.strip() for chunk in chunks)
    
    def extract_from_file_sync(self, file_path: str) -> str:
        """
        Synchronous wrapper for the async extract_from_file function.
        """
        return asyncio.run(self.extract_from_file(file_path))
        
#####    Example Usage    #####
# processor = FileProcessor()
# content = processor.extract_from_file_sync("data/ZacharyBiery_CV_2024.docx")
# print(content)
