def foo(**kwargs):
    print("args:", kwargs, "type:", type(kwargs))
    [print(k, v) for k, v in kwargs.items()]


if __name__ == "__main__":
    arr = ["a", "b", "c", "d", "e"]
    print(arr)
    print(arr[2:])
    print(arr[-3:])
