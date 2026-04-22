import json
from pathlib import Path
from typing import Dict, Any, Union


class DataLoader:
    def __init__(self, data_path: str):
        self.base_path = Path(data_path)

    def _load_json(self, filename: str) -> Dict[str, Any]:
        with open(self.base_path / filename, "r", encoding="utf-8") as f:
            return json.load(f)


    def get_market_data(self) -> Dict:
        return self._load_json("market_data.json")


    def get_news(self) -> list:
        data = self._load_json("news_data.json")
        return data.get("news", [])


    def get_portfolios(self) -> Union[Dict, list]:
        data = self._load_json("portfolios.json")
        return data.get("portfolios", {})


    def get_portfolio(self, portfolio_id: str) -> Dict:
        portfolios = self.get_portfolios()

        # Case 1: dict
        if isinstance(portfolios, dict):
            return portfolios.get(portfolio_id)

        # Case 2: list
        elif isinstance(portfolios, list):
            return next(
                (p for p in portfolios if p.get("id") == portfolio_id),
                None
            )

        raise ValueError("Unsupported portfolio structure")