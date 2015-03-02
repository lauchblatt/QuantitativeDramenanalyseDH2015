def average(list_of_numbers):
    if(len(list_of_numbers) >= 1):
        return float(sum(list_of_numbers))/len(list_of_numbers)
    else:
        return float("nan")

def median(list_of_numbers):
    sortedLst = sorted(list_of_numbers)
    lstLen = len(list_of_numbers)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0