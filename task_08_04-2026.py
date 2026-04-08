def average_marks(marks):
    if len(marks) == 0:
        return "no data"
    total = sum(marks)
    avg=total / len(marks)
    return avg
print(average_marks([50, 60, 80, 90, 76]))
print(average_marks([]))
