# Contributing to ComponentOS

Thanks for helping improve ComponentOS. Contributions can include code, documentation, examples, tests, hardware integrations, and troubleshooting knowledge.

## Before you start

1. Search existing issues and pull requests.
2. For substantial changes, open an issue first so the design can be discussed.
3. Never commit API keys, `.env` files, device credentials, private datasheets, or production firmware secrets.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
```

Use Ollama or a test/mocked provider when possible so tests do not depend on a paid or rate-limited service.

## Pull requests

- Keep changes focused and explain the user impact.
- Add or update tests and documentation when behavior changes.
- Include the board, peripheral, and provider details for hardware-related changes.
- Do not include generated secrets or personal device logs.
- Confirm that generated code is reviewed and that safety checks remain enabled.
- Use the pull request template and ensure automated checks pass.

## Commit and code style

Use clear, imperative commit messages such as `Add SPI sensor example`. Follow the existing Python style, prefer small functions, and keep provider-specific behavior behind the provider abstraction.

## Reporting issues

Use the templates under `.github/ISSUE_TEMPLATE/`. Questions and usage help belong in [Discussions](https://github.com/IceCheetah9418/componentOS/discussions); reproducible defects belong in Issues.

By contributing, you agree that your contributions are provided under the repository's MIT License.
