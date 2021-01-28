
def sumMultiplesBelow(belowNumber: int, *multiplesOf: int):
    filteredNumbers = [i for i in range(1, belowNumber)
                        if any((i % divisor == 0) for divisor in multiplesOf)]
    return sum(filteredNumbers)
