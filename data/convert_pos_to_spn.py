def convert_pos_to_spn(upper, lower):
    upper = list(map(lambda x: float(x), upper.split()))
    lower = list(map(lambda x: float(x), lower.split()))
    return [str(abs(upper[0] - lower[0])), str(abs(upper[1] - lower[1]))]