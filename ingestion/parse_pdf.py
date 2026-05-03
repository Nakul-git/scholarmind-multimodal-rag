import os
import json
import fitz

from ingestion.image_reasoning import analyze_image_with_llava


IMAGE_DIR = "data/images"
PARSED_DIR = "data/parsed"


def parse_pdf(pdf_path: str, paper_metadata: dict):
    """
    Extract:
    - page text
    - images
    - LLaVA image summaries

    Returns parsed items.
    """

    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(PARSED_DIR, exist_ok=True)

    paper_id = paper_metadata["paper_id"]
    paper_image_dir = os.path.join(IMAGE_DIR, paper_id)
    os.makedirs(paper_image_dir, exist_ok=True)

    doc = fitz.open(pdf_path)

    parsed_items = []

    for page_index, page in enumerate(doc):
        page_number = page_index + 1

        print(f"📄 Parsing page {page_number}")

        # -------------------------
        # Extract text
        # -------------------------
        page_text = page.get_text()

        if page_text.strip():
            parsed_items.append({
                "content": page_text,
                "type": "text",
                "page": page_number,
                "source": pdf_path,
                "paper_id": paper_id,
                "title": paper_metadata["title"]
            })

        # -------------------------
        # Extract images
        # -------------------------
        images = page.get_images(full=True)

        for image_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_path = os.path.join(
                paper_image_dir,
                f"page_{page_number}_image_{image_index + 1}.{image_ext}"
            )

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            print(f"🖼️ Extracted image: {image_path}")
            print("👁️ Sending image to LLaVA...")

            image_summary = analyze_image_with_llava(image_path)

            if image_summary.strip():
                parsed_items.append({
                    "content": image_summary,
                    "type": "image_reasoning",
                    "page": page_number,
                    "source": pdf_path,
                    "paper_id": paper_id,
                    "title": paper_metadata["title"],
                    "image_path": image_path
                })

    # Save parsed JSON
    parsed_json_path = os.path.join(PARSED_DIR, f"{paper_id}.json")

    with open(parsed_json_path, "w", encoding="utf-8") as f:
        json.dump(parsed_items, f, indent=2, ensure_ascii=False)

    print(f"✅ Parsed file saved: {parsed_json_path}")

    return parsed_items