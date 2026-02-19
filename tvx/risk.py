def normalize(score):
    return min(100, max(0, score))

def level(score):
    score = normalize(score)
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"
