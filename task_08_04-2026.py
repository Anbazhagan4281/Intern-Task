def average_marks(marks):
    if len(marks) == 0:
        return "no data"
    total = sum(marks)
    avg=total / len(marks)
    return avg
print("average=",average_marks([72, 85, 90, 78, 88]))
