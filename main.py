"""Use a custom model endpoint with Copilot. Run with: uv run main.py."""

import asyncio
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from azure.identity.aio import AzureCliCredential
from copilot import CopilotClient
from copilot.session import PermissionHandler, ProviderTokenArgs
from dotenv import load_dotenv

async def main() -> None:
    """Send a request to your model and print the complete response."""
    load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)
    base_url = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

    async with AzureCliCredential() as credential:

        async def get_bearer_token(_args: ProviderTokenArgs) -> str:
            token = await credential.get_token(
                "https://ai.azure.com/.default"
            )
            return token.token

        async with CopilotClient() as client, await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model=os.environ["FOUNDRY_MODEL"],
            provider={
                "type": "openai",
                "base_url": base_url,
                "wire_api": "responses",
                "bearer_token_provider": get_bearer_token,
            },
            streaming=False,
        ) as session:
            response = await session.send_and_wait("Tell me a tech joke.")
            if response is None:
                raise RuntimeError("Copilot completed the request without an assistant message.")
            print(response.data.content)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(130)
