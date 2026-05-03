from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -------------------------------
# Detect research paper sections
# -------------------------------
SECTION_KEYWORDS = [
    "abstract",
    "introduction",
    "related work",
    "background",
    "method",
    "methodology",
    "approach",
    "model",
    "experiments",
    "results",
    "discussion",
    "conclusion",
    "references"
]


def detect_sections(text: str):
    """
    Split text into sections based on common research headings.
    """

    sections = []
    current_section = "unknown"
    buffer = []

    lines = text.split("\n")

    for line in lines:
        clean_line = line.strip().lower()

        # Check if this line is a section header
        if any(keyword == clean_line for keyword in SECTION_KEYWORDS):
            if buffer:
                sections.append((current_section, "\n".join(buffer)))
                buffer = []

            current_section = clean_line
        else:
            buffer.append(line)

    # Add last section
    if buffer:
        sections.append((current_section, "\n".join(buffer)))

    return sections


# -------------------------------
# Main chunking function
# -------------------------------
def chunk_documents(parsed_items):
    """
    Convert parsed text + LLaVA image summaries into structured chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150
    )

    final_docs = []

    for item in parsed_items:

        content = item["content"]
        item_type = item.get("type")

        # ---------------------------------
        # 🖼️ IMAGE CHUNKS (DO NOT SPLIT)
        # ---------------------------------
        if item_type == "image_reasoning":
            doc = Document(
                page_content=content,
                metadata={
                    "type": item_type,
                    "section": "figure",
                    "page": item.get("page"),
                    "source": item.get("source"),
                    "paper_id": item.get("paper_id"),
                    "title": item.get("title"),
                    "image_path": item.get("image_path"),
                    "chunk_index": 0
                }
            )
            final_docs.append(doc)
            continue

        # ---------------------------------
        # 📄 TEXT CHUNKS (SECTION-AWARE)
        # ---------------------------------
        sections = detect_sections(content)

        for section_name, section_text in sections:

            # Skip empty sections
            if not section_text.strip():
                continue

            # If section small → keep as single chunk
            if len(section_text) < 900:
                chunks = [section_text]
            else:
                # Recursive splitting for large sections
                chunks = splitter.split_text(section_text)

            # Create documents
            for chunk_index, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "type": item_type,
                        "section": section_name,
                        "page": item.get("page"),
                        "source": item.get("source"),
                        "paper_id": item.get("paper_id"),
                        "title": item.get("title"),
                        "image_path": item.get("image_path"),
                        "chunk_index": chunk_index
                    }
                )

                final_docs.append(doc)

    print(f"✅ Total chunks created: {len(final_docs)}")

    return final_docs