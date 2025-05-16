import yaml
import logging
import argparse
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_yaml(filepath: str):
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load YAML: {e}")
        return {}

def check_routing_expiry(data: dict, notice_period_days: int):
    today = datetime.today().date()
    producers = data.get('producers', [])

    if not producers:
        logger.warning("No producers found.")
        return 0

    warnings = 0

    for producer in producers:
        if not producer or 'consumer_list' not in producer:
            continue

        for consumer in producer['consumer_list']:
            for _, c in consumer.items():
                name = c.get('name', 'Unknown')
                start_date = c.get('start_date')
                routing_period = c.get('routing_period')
                contacts = c.get('contacts', [])

                if not start_date or not routing_period:
                    logger.warning(f"Skipping consumer '{name}' due to missing info.")
                    continue

                try:
                    start = datetime.strptime(start_date, '%Y-%m-%d').date()
                    expiry = start + timedelta(days=int(routing_period))
                    days_left = (expiry - today).days

                    if days_left <= notice_period_days:
                        logger.warning(f" Routing for '{name}' expires in {days_left} days on {expiry}.")
                        for contact in contacts:
                            logger.info(f"   ➤ Notify: {contact}")
                        warnings += 1

                except Exception as e:
                    logger.error(f"Error with consumer '{name}': {e}")

    return warnings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check routing expiry")
    parser.add_argument("--action", required=True, choices=["check_routing_expiry"])
    parser.add_argument("--yaml", default="routing_data.yaml")
    parser.add_argument("--days", type=int, default=15)

    args = parser.parse_args()

    if args.action == "check_routing_expiry":
        data = load_yaml(args.yaml)
        warning_count = check_routing_expiry(data, args.days)
        if warning_count > 0:
            exit(1)
