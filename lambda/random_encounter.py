import json
import random
import urllib.parse
import urllib.request
import uuid
from datetime import datetime
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr

# DynamoDB Setup
DDB = boto3.resource('dynamodb')
monsters_table = DDB.Table("Monsters")
encounters_table = DDB.Table("Encounters")

# noinspection PyUnusedLocal
def handler(event, context):
    # Get level from query parameters
    level = event.get("queryStringParameters", {}).get("level", "1")
    try:
        level = float(level)
    except ValueError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid level parameter"}),
            "headers": {"Content-Type": "application/json"},
        }

    # Build Open5e query
    base_url = "https://api.open5e.com/v1/monsters/"
    params = urllib.parse.urlencode({"challenge_rating": level})
    url = f"{base_url}?limit=50&{params}&document__slug=wotc-srd"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            monsters = data.get("results", [])

            # print("Fetched from Open5E", data)

            if not monsters:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"message": "No monsters found"}),
                    "headers": {"Content-Type": "application/json"},
                }
            chosen = random.choice(monsters)
            print(chosen)
            slug = chosen["slug"]

            # Check if the monster is in the Monsters table
            existing = monsters_table.scan(
                FilterExpression=Attr("slug").eq(slug)
            )
            if not existing.get("Items"):
                new_item = {
                    "id": f"m-{uuid.uuid4().hex[:8]}",
                    "slug": slug,
                    "name": chosen["name"],
                    "cr": Decimal(str(chosen["challenge_rating"])),
                    "hp": chosen["hit_points"],
                    "ac": chosen["armor_class"],
                    "type": chosen["type"],
                    "source": "open5e"
                }
                monsters_table.put_item(Item={
                    "id": new_item["id"],
                    "monster_id": new_item["slug"],
                    "timestamp": datetime.now()
                })

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "name": chosen["name"],
                    "slug": slug,
                    "cr": chosen["challenge_rating"],
                    "hp": chosen["hit_points"],
                    "ac": chosen["armor_class"],
                    "type": chosen["type"],
                }),
                "headers": {"Content-Type": "application/json"},
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }
