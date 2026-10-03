import argparse

from rag.pipeline import RagPipeline


def main():
    parser = argparse.ArgumentParser(description="PDF + Excel RAG")
    commands = parser.add_subparsers(dest="command", required=True)

    ingest_command = commands.add_parser("ingest")
    ingest_command.add_argument("--vision", action="store_true")

    search_command = commands.add_parser("search")
    search_command.add_argument("question")

    ask_command = commands.add_parser("ask")
    ask_command.add_argument("question")

    args = parser.parse_args()
    rag = RagPipeline()

    if args.command == "ingest":
        count = rag.ingest(use_vision=args.vision)
        print(f"Indexed {count} chunks.")

    elif args.command == "search":
        documents = rag.search(args.question)

        for number, doc in enumerate(documents, start=1):
            print(f"\n[{number}] {doc.metadata}")
            print(doc.page_content[:500])

    elif args.command == "ask":
        print(rag.ask(args.question))


if __name__ == "__main__":
    main()