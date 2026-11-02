"""Use a custom model endpoint with Copilot. Run with: uv run main.py."""

import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def _configure_monitoring() -> logging.Logger:
    logger_name = "hello_copilot_harness"
    if os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        from microsoft.opentelemetry import use_microsoft_opentelemetry

        use_microsoft_opentelemetry(
            enable_azure_monitor=True,
            logger_name=logger_name,
        )
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    return logger


async def main() -> None:
    """Send a request to your model and print the complete response."""
    load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)
    logger = _configure_monitoring()

    from azure.identity.aio import AzureCliCredential
    from copilot import CopilotClient
    from copilot.session import PermissionHandler, ProviderTokenArgs

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
            logger.info("Sending request to model %s", os.environ["FOUNDRY_MODEL"])
            try:
                response = await session.send_and_wait("Tell me a tech joke.")
                if response is None:
                    raise RuntimeError(
                        "Copilot completed the request without an assistant message."
                    )
            except Exception:
                logger.exception("Model request failed.")
                raise

            logger.info("Model request completed.")
            print(response.data.content)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(130)
