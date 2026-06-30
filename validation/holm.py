def holm_correct(p_values, alpha=0.05) -> dict:
    """
    p_values: {pair name: p_value} dicts (10 pairs)
    Holm-Bonferroni correction. Returns: {pairs name: (correction p, significance)}
    """

    items = sorted(p_values.items(), key=lambda kv: kv[1])
    m = len(items)

    results = {}
    max_p_so_far = 0

    for rank, (name, p) in enumerate(items):
        adjusted = (m - rank) * p
        adjusted = min(1, adjusted)
        max_p_so_far = max(max_p_so_far, adjusted)
        results[name] = (max_p_so_far, max_p_so_far < alpha)

    return results