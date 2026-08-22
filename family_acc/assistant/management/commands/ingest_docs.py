# family_acc/assistant/management/commands/ingest_docs.py
import os
import re
from django.core.management.base import BaseCommand
from openai import OpenAI
from assistant.models import UIDocumentationChunk


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
            text = raw_chunk.strip()
            if not text:
                continue

            lines = text.split("\n")
            title = lines[0].lstrip("#").strip() if lines[0].startswith("#") else ""

            response = client.embeddings.create(
                input=text, model=deployment_name, dimensions=512
            )
            embedding_vector = response.data[0].embedding

            UIDocumentationChunk.objects.create(
                source_file=file_name,
                category=category,
                title=title,
                content=text,
                embedding=embedding_vector,
            )
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully ingested {created_count} chunks from '{file_name}' ({category})!"
            )
        )