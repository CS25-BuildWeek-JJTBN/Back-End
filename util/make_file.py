f = open('questions.txt', 'r')
w = open('questions2.txt', 'w')
arr = f.read().split(',')
idx = 0
while idx < len(arr)-1:
    w.write(arr[idx] + "," + arr[idx+1] + "\n")
    idx += 2
f.close()
w.close()