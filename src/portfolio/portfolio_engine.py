from typing import Dict, List


class PortfolioEngine:
    """
    Handles:
    - P&L computation
    - Sector allocation
    - Asset type allocation
    - Risk detection
    """


    # P&L CALCULATION

    def compute_pnl(self, holdings: List[Dict]) -> Dict:
        total_value = 0.0
        total_pnl = 0.0

        for h in holdings:
            price = float(h.get("current_price", 0))
            qty = float(h.get("quantity", 0))
            change_pct = float(h.get("day_change_percent", 0))

            value = price * qty
            pnl = value * (change_pct / 100)

            total_value += value
            total_pnl += pnl

        pnl_pct = (total_pnl / total_value * 100) if total_value else 0.0

        return {
            "total_value": round(total_value, 2),
            "pnl": round(total_pnl, 2),
            "pnl_percent": round(pnl_pct, 2)
        }


    # SECTOR ALLOCATION 

    def sector_allocation(self, holdings: List[Dict]) -> Dict:
        allocation: Dict[str, float] = {}

        for h in holdings:
            sector = h.get("sector", "UNKNOWN")
            weight = float(h.get("weight_in_portfolio", 0))

            allocation[sector] = allocation.get(sector, 0) + weight

        return {k: round(v, 2) for k, v in allocation.items()}


    # ASSET TYPE ALLOCATION 


    def asset_allocation(self, holdings: List[Dict]) -> Dict:
        allocation = {"STOCK": 0.0, "MUTUAL_FUND": 0.0}

        for h in holdings:
            asset_type = h.get("type", "STOCK")
            weight = float(h.get("weight_in_portfolio", 0))

            allocation[asset_type] = allocation.get(asset_type, 0) + weight

        return {k: round(v, 2) for k, v in allocation.items()}


    # RISK DETECTION 

    def detect_risk(self, holdings: List[Dict], sector_alloc: Dict) -> List[str]:
        risks = []

        # 1. Sector concentration risk
        for sector, weight in sector_alloc.items():
            if weight > 40:
                risks.append(f"High sector concentration: {sector} ({weight:.2f}%)")

        # 2. Single stock concentration risk
        for h in holdings:
            weight = float(h.get("weight_in_portfolio", 0))
            symbol = h.get("symbol", "UNKNOWN")

            if weight > 20:
                risks.append(f"High single-stock exposure: {symbol} ({weight:.2f}%)")

        # 3. Unknown sector risk
        if "UNKNOWN" in sector_alloc:
            risks.append("Some holdings have unknown sector classification")

        return risks if risks else ["No major concentration risks"]