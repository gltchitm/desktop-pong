def near(left, right, leeway):
    return True if left == right else abs(left - right) <= leeway
