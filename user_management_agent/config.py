import logging
import os

from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4o-mini")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.2"))
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
MCP_SERVER_NAME = os.getenv("MCP_SERVER_NAME", "User Management MCP")

print(f"Using model: {MODEL} with temperature: {MODEL_TEMPERATURE}")
print(f"MCP Server URL: {MCP_SERVER_URL}")
print(f"MCP Server Name: {MCP_SERVER_NAME}")

