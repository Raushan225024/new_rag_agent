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


def connect_supabase():

    global supabase

    try:

        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL or SUPABASE_KEY is missing"
            )

        # Create Supabase client
        supabase = create_client(
            SUPABASE_URL,
            SUPABASE_KEY
        )

        # Test database connection
       

        print("Supabase connection established")

        return supabase

    except Exception as e:

        print("Supabase connection failed")
        print(f"Error: {e}")

        supabase = None

        return None