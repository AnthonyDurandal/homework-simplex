import functools

def compare_nums(num1, num2):
    return -1 if num1<num2 else 1

if __name__ == "__main__":
    print(sorted([5,4,3,2,1], key=functools.cmp_to_key(compare_nums)))