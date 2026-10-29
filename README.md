---
title: Hello Copilot Harness
description: A minimal Python example that prints a complete response from GitHub Copilot.
---

## What it does

Starts a Copilot client, creates a non-streaming session using your own
model endpoint and Azure CLI credentials, asks for a tech joke, and prints the complete response.
Async context managers close the session and client, including when a request fails.

## Prerequisites

* Python 3.11 or later
* [uv](https://docs.astral.sh/uv/getting-started/installation/)
* [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), signed in with `az login`
* An Azure OpenAI model deployment supporting the Responses API
* The `Cognitive Services OpenAI User` role (or another role granting inference access)
  assigned to your Azure identity on the Azure OpenAI resource

Bring-your-own-key (BYOK) mode does not require GitHub Copilot authentication.
The SDK can download its bundled runtime on first use, which requires network access.

## Set up and run

Run these commands in PowerShell from this folder:

```powershell
uv sync
```

Set the endpoint and deployment name in a `.env` file next to [main.py](main.py):

```dotenv
FOUNDRY_PROJECT_ENDPOINT=https://<resource-name>.openai.azure.com/openai/v1/
FOUNDRY_MODEL=<your-deployment-name>
```

Sign in and run:

```powershell
az login
uv run main.py
```

Use your deployment name, which may differ from the underlying model name.
Supply the base URL ending in `/openai/v1/`, not `/responses`.
For a Foundry resource using the `services.ai.azure.com` hostname, use
`https://<resource-name>.services.ai.azure.com/openai/v1/`.
Despite the variable name, `FOUNDRY_PROJECT_ENDPOINT` must contain the model
inference base URL, not an `/api/projects/<project-name>` URL.
The script passes this value directly to the provider without converting it.
The code uses `wire_api="responses"`; change it to `"completions"` for a
deployment that requires Chat Completions instead.
Both configuration variables are required. Missing variables raise a `KeyError`;
blank values are not validated by the script.
The script loads `.env` from its own folder, even when run from another directory.
Existing environment variables take precedence over values in `.env`.
The `.env` file is ignored by Git.
No API key or `FOUNDRY_API_KEY` variable is needed.
`AzureCliCredential` uses the account signed in through Azure CLI, not a VS Code
sign-in. For another tenant, use `az login --tenant <tenant-id>`.
The token callback requests Azure OpenAI access tokens for
`https://ai.azure.com/.default` on demand, so a long-lived session
does not rely on a single static token.
If authentication fails, check `az login`. A 403 can indicate missing inference
permissions or resource network restrictions; role assignments can take time to propagate.

`uv sync` creates the local `.venv` and installs the dependencies.
The project uses Microsoft's Python package proxy, configured in
[pyproject.toml](pyproject.toml), because direct PyPI downloads fail on this network.
The SDK is pinned to `1.0.25`, the newest stable version available in that mirror
when this example was set up.
Development dependencies include notebook support, Ruff, tqdm, and pytest;
the example itself uses `github-copilot-sdk`, `azure-identity`, and `python-dotenv`.

You can also run the environment's Python directly, without activating it:

```powershell
.\.venv\Scripts\python.exe main.py
```

To activate the environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Change the prompt passed to `send_and_wait` in [main.py](main.py) to try another request.
Requests are billed through your model provider rather than your Copilot subscription.

> [!WARNING]
> This example keeps `PermissionHandler.approve_all` from the starting snippet.
> It automatically approves tool permissions, including file and command access.
> Run it only in a trusted folder with trusted prompts.

## Reference

* [Copilot SDK getting started](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md)
* [Copilot SDK BYOK configuration](https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md)
