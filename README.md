# Encounter Generator API

A lightweight, AWS-hosted backend service for generating Dungeons & Dragons 5e encounters based on player level. Supports streaming integration, custom homebrew monsters, and historical encounter tracking.

---

## Features

- Dynamic encounter generation by level
- Integration with Open5e monster data
- Custom homebrew monster support
- Smart groupings for lower CR monsters
- Encounter history tracking
- Twitch streaming integration (via chatbot)
- Serverless backend powered by AWS Lambda, API Gateway, and DynamoDB
- Managed with Pulumi (Infrastructure-as-Code)

---

## Deployment Instructions

### 1. Install Dependencies

Make sure you have these installed:
- Python 3.12+
- [Pulumi CLI](https://www.pulumi.com/docs/get-started/install/)
- AWS CLI with valid credentials

### 2. Set up Python environment

```bash
cd lambda
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Pulumi stack

```bash
pulumi login
pulumi stack init dev
pulumi config set aws:region us-east-1
```

### 4. Deploy the stack

```bash
pulumi up
```

---

## Usage (Local Test)

To test the handler locally:

```bash
python lambda/handler.py
```

Once deployed, try hitting the endpoint:

```bash
curl "https://<your-api-url>/encounter?level=3"
```

---

## Example Output

```json
{
  "name": "Goblin Ambush",
  "monsters": [
    {"name": "Goblin", "cr": 0.25},
    {"name": "Goblin", "cr": 0.25},
    {"name": "Goblin Boss", "cr": 1}
  ],
  "environment": "forest"
}
```

---

## Future Plans

- Add biome-based encounter filters (forest, swamp, dungeon)
- Include treasure/reward generation
- Roll20 / Foundry export integration
- Encounter balancing tools for solo/party mode

---

## License

MIT License. See `LICENSE` for details.
