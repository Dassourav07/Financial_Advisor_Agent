class Evaluator:
    
    def score(self, explanation: str) -> float:
        explanation = explanation.lower()

        score = 0.0

 
        # 1. Causal reasoning (0.25)
 
        if "causal chain" in explanation:
            score += 0.25

 
        # 2. Contribution analysis (0.25)
 
        contrib_count = explanation.count("contributed")
        if contrib_count >= 3:
            score += 0.25
        elif contrib_count == 2:
            score += 0.18
        elif contrib_count == 1:
            score += 0.1

 
        # 3. Conflict handling (0.2)
 
        if "conflicting" in explanation:
            score += 0.2

 
        # 4. Sector awareness
 
        if "sector" in explanation:
            score += 0.15

 
        # 5. Macro linkage 
 
        if "macro" in explanation or "rbi" in explanation:
            score += 0.15


        if explanation.count("primary driver") <= 1:
            score -= 0.05

        if "fii" not in explanation and "global" not in explanation:
            score -= 0.05

        # Clamp score
        return round(max(0, min(score, 1.0)), 2)