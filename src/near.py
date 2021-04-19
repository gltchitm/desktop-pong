def near(left, right, leeway):
    if left > right:
        return abs(right - left) <= leeway
    elif left < right:
        return abs(left - right) <= leeway
    else:
        return True
