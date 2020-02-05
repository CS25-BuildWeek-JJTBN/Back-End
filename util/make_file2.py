with open('questions.txt', 'r') as f:
    arr = f.read().split(',')
    with open('questions2.txt', 'w') as w:
        idx = 0
        while idx < len(arr) - 1:
            w.write(f"{arr[idx].strip()}, {arr[idx + 1]}\n")
            idx += 2