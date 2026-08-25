# family_acc/assistant/management/commands/ingest_docs.py
import os
import re
from django.core.management.base import BaseCommand
from openai import OpenAI
from assistant.models import UIDocumentationChunk


def clean_and_format_chunk(raw_chunk: str) -> tuple[str, str]:
    """
    Cleans raw Markdown chunk by extracting titles, stripping heavy header syntax,
    removing horizontal dividers, and prepending lightweight contextual metadata.
    Returns a tuple of (extracted_title, cleaned_text).
    """
    text = raw_chunk.strip()
    if not text:
        return "", ""

    lines = text.split("\n")
    
    # Extract header title if present
    extracted_title = ""
    if lines[0].startswith("#"):
        extracted_title = lines[0].lstrip("#").strip()
        # Remove the header line from the body
        lines = lines[1:]
    
    cleaned_body = "\n".join(lines)

    # 1. Remove Markdown horizontal lines (---, ***, ___)
    cleaned_body = re.sub(r"^\s*[-*_]{3,}\s*$", "", cleaned_body, flags=re.MULTILINE)
    
    # 2. Downgrade/strip internal header markers inside the body to plain bold text
    # Turns "### Step 1: Open page" into "**Step 1: Open page**"
    cleaned_body = re.sub(r"^\s*#{1,6}\s*(.+)$", r"**\1**", cleaned_body, flags=re.MULTILINE)

    # 3. Normalize multiple trailing blank lines
    cleaned_body = re.sub(r"\n{3,}", "\n\n", cleaned_body).strip()

    # 4. Prepend lightweight context for the embedding & LLM (instead of raw # headers)
    if extracted_title:
        final_text = f"[Context: {extracted_title}]\n{cleaned_body}".strip()
    else:
        final_text = cleaned_body

    return extracted_title, final_text

class Command(BaseCommand):
    help = "Ingests a specific Markdown document into pgvector."

    def add_arguments(self, parser):
        parser.add_argument("md_file_path", type=str, help="Path to the .md file")
        parser.add_argument(
            "--category",
            type=str,
            choices=["ui", "api", "general"],
            default="general",
            help="Category tag for filtering",
        )

    def handle(self, *args, **options):
        file_path = options["md_file_path"]
        category = options["category"]
        file_name = os.path.basename(file_path)

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        deployment_name = os.getenv("OPEN_AI_EMBEDDING_DEPLOYMENT")
        client = OpenAI(
            base_url = os.getenv("OPEN_AI_ENDPOINT"),
            api_key = os.getenv("OPEN_AI_API_KEY"),
        )

        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        raw_chunks = re.split(r"(?=\n#+\s)", raw_text)

        # Delete ONLY existing chunks from THIS specific file
        deleted_count, _ = UIDocumentationChunk.objects.filter(
            source_file=file_name
        ).delete()
        self.stdout.write(
            self.style.WARNING(
                f"Cleared {deleted_count} existing chunks for '{file_name}'."
            )
        )

        created_count = 0
        for raw_chunk in raw_chunks:
            title, cleaned_text = clean_and_format_chunk(raw_chunk)
            
            if not cleaned_text:
                continue

            # Embed the preprocessed context string
            response = client.embeddings.create(
                input=cleaned_text, model=deployment_name, dimensions=512
            )
            embedding_vector = response.data[0].embedding

            UIDocumentationChunk.objects.create(
                source_file=file_name,
                category=category,
                title=title,
                content=cleaned_text,
                embedding=embedding_vector,
            )
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully ingested {created_count} chunks from '{file_name}' ({category})!"
            )
        )