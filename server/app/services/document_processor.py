import re
from typing import Any


class DocumentParser:
    def parse(self, content: bytes, filename: str) -> list[dict[str, Any]]:
        text = self._extract_text(content, filename)
        return [{"page_content": text, "filename": filename}]

    def _extract_text(self, content: bytes, filename: str) -> str:
        ext = filename.lower().split(".")[-1]
        if ext == "pdf":
            return self._parse_pdf(content)
        elif ext in ("txt", "md"):
            return content.decode("utf-8", errors="ignore")
        return content.decode("utf-8", errors="ignore")

    def _parse_pdf(self, content: bytes) -> str:
        text = ""
        try:
            import pypdf
            from io import BytesIO
            reader = pypdf.PdfReader(BytesIO(content))
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                text += f"\n--- Page {page_num} ---\n{page_text}"
        except ImportError:
            text = content.decode("utf-8", errors="ignore")
        return text


class ChunkProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
        chunks = []
        for doc in documents:
            text = doc["page_content"]
            filename = doc["filename"]
            page_match = re.search(r"--- Page (\d+) ---", text)
            page_number = int(page_match.group(1)) if page_match else 1

            text_parts = re.split(r"--- Page \d+ ---", text)
            for part_idx, part in enumerate(text_parts):
                if not part.strip():
                    continue
                part_chunks = self._split_text(part, filename, page_number, part_idx)
                chunks.extend(part_chunks)
        return chunks

    def _split_text(self, text: str, filename: str, page_number: int, part_index: int) -> list[dict[str, Any]]:
        chunks = []
        separator = "\n"
        if not text or text.isspace():
            return chunks

        chars = list(text)
        start = 0
        chunk_index = 0

        while start < len(chars):
            end = min(start + self.chunk_size, len(chars))
            while end > start and chars[end - 1] not in separator:
                end -= 1
            if end == start:
                end = min(start + self.chunk_size, len(chars))

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "page_content": chunk_text,
                    "metadata": {
                        "page_number": page_number,
                        "source_filename": filename,
                        "chunk_index": chunk_index,
                        "part_index": part_index
                    }
                })
                chunk_index += 1

            start = end - self.chunk_overlap if end > self.chunk_overlap else end

        return chunks
