import hashlib
from difflib import SequenceMatcher


# -----------------------------
# 1. Exact duplicate removal
# -----------------------------
def remove_exact_duplicates(docs):
    """
    Removes exact duplicate chunks using hash.
    """

    seen_hashes = set()
    unique_docs = []

    for doc in docs:
        text = doc.page_content.strip()

        text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()

        if text_hash not in seen_hashes:
            seen_hashes.add(text_hash)
            unique_docs.append(doc)

    print(f"🧹 Exact dedup: {len(docs)} → {len(unique_docs)}")

    return unique_docs


# -----------------------------
# 2. Near duplicate removal
# -----------------------------
def is_similar(text1, text2, threshold=0.9):
    """
    Returns True if texts are very similar.
    """
    return SequenceMatcher(None, text1, text2).ratio() > threshold


def remove_near_duplicates(docs, threshold=0.9):
    """
    Removes near-duplicate chunks (similar content).
    """

    unique_docs = []

    for doc in docs:
        text = doc.page_content.strip()

        duplicate_found = False

        for existing_doc in unique_docs:
            if is_similar(text, existing_doc.page_content, threshold):
                duplicate_found = True
                break

        if not duplicate_found:
            unique_docs.append(doc)

    print(f"🧠 Near dedup: {len(docs)} → {len(unique_docs)}")

    return unique_docs


# -----------------------------
# 3. Image duplicate skipping
# -----------------------------
def remove_duplicate_images(parsed_items):
    """
    Remove duplicate images using hash of image_path.
    """

    seen_images = set()
    filtered_items = []

    for item in parsed_items:
        if item.get("type") == "image_reasoning":
            image_path = item.get("image_path")

            if not image_path:
                continue

            image_hash = hashlib.md5(image_path.encode()).hexdigest()

            if image_hash in seen_images:
                continue

            seen_images.add(image_hash)

        filtered_items.append(item)

    print(f"🖼️ Image dedup: {len(parsed_items)} → {len(filtered_items)}")

    return filtered_items