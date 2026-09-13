import os
import logging

from supabase import create_client, Client # type: ignore
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Validate environment variables
if not SUPABASE_URL:
    logger.error("SUPABASE_URL is not set in .env")

if not SUPABASE_KEY:
    logger.error("SUPABASE_KEY is not set in .env")


supabase: Client | None = None


# Create Supabase client
try:

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "Missing Supabase environment variables"
        )

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    logger.info("Supabase client created successfully")


except Exception as e:

    logger.error(
        f"Failed to create Supabase client: {e}"
    )


# Test database connection
def test_supabase_connection():

    if supabase is None:
        logger.error(
            "Supabase client is not initialized"
        )
        return False

    try:

        response = (
            supabase
            .table("documents")
            .select("id")
            .limit(1)
            .execute()
        )

        logger.info(
            "Supabase database connected successfully"
        )

        return True

    except Exception as e:

        logger.error(
            f"Supabase database connection failed: {e}"
        )

        return False