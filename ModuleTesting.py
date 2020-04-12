# This is testing the CheckCollision module in the main.py file

def CheckCollision(arr, coord):
    x1, y1, x2, y2, counter = 0, 0, 0, 0, 0
    for i in arr:
        x1, y1, x2, y2 = i[0], i[1], i[2], i[3]
        if x1 <= coord [0] and x2 >= coord[0]:
            if y1 <= coord [1] and y2 >= coord[1]:
                return False
        else:
            counter +=1 
    if counter == len(arr):
        return True

arr = [[600,0,6,606]]
pos = (5, 585)
print(CheckCollision(arr, pos))
