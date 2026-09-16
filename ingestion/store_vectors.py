from pathlib import Path
import sys

# Ensure `rag` (the parent folder) is on sys.path
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from config.vector_db_config import connect_supabase


def upload_batch_data(
    vector,
    batch_size=10
):

    # Establish connection
    supabase = connect_supabase()

    if supabase is None:

        print("Upload cancelled: Supabase is not connected")

        return False

    if not vector:

        print("No data available for upload")

        return False

    total_records = len(vector)

    print(f"Total records: {total_records}")
    print(f"Batch size: {batch_size}")

    uploaded_records = 0

    try:

        # Divide data into batches
        for start in range(0, total_records, batch_size):

            end = start + batch_size

            batch_vector = vector[start:end]

            # Prepare batch data
            batch = [
                {
                    "embedding": vec
                }
                for vec in batch_vector
            ]

            print(
                f"\nUploading batch: "
                f"{start + 1} - "
                f"{min(end, total_records)}"
            )

            # Insert batch into Supabase
            response = (
                supabase
                .table("document_vector")
                .insert(batch)
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

        print("\nError during batch upload")

        print(f"Error: {e}")

        print(
            f"Uploaded before failure: "
            f"{uploaded_records}"
        )

        return False