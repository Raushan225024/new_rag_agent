from pathlib import Path
import sys

# Ensure `rag` (the parent folder) is on sys.path
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from config.vector_db_config import connect_supabase


def upload_content(
    chunks,
    batch_size=1
):

    # Establish connection
    supabase = connect_supabase()

    if supabase is None:

        print("Upload cancelled: Supabase is not connected")

        return False

    if not chunks:

        print("No data available for upload")

        return False

    total_records = len(chunks)

    print(f"Total records: {total_records}")
    print(f"Batch size: {batch_size}")

    uploaded_records = 0

    try:

        # Divide data into batches
        for start in range(0, total_records, batch_size):

            end = start + batch_size
            chunk_start = start
            end = min(end, total_records)
            

            batch_chunks = chunks[start:end]

            # Prepare batch data
            batch = [
                {
                    "content": chunk
                }
                for chunk in batch_chunks
            ]

            print(
                f"\nUploading batch: "
                f"{start + 1} - "
                f"{min(end, total_records)}"
            )
            row_ids = list(
                    range(chunk_start + 1, end + 1)
                )
            # Insert batch into Supabase
            response = (
                supabase
                .table("document_vector")
                .update(batch)
                .in_("id", row_ids)
                .execute()
            )

            uploaded_records += len(batch)

            print(
                f"Batch uploaded successfully: "
                f"{len(batch)} records"
            )

        print("\nAll data uploaded successfully")

        print(
            f"Total uploaded: "
            f"{uploaded_records}"
        )

        return True

    except Exception as e:

        print("\nError during batch_content upload")

        print(f"Error: {e}")

        print(
            f"Uploaded before failure: "
            f"{uploaded_records}"
        )

        return False