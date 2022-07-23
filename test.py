message=[]
done=False
while not done:
    temp = input()
    if len(temp) != 0 and temp[-1] == "~":
        done = True
        message.append(temp[:-1])
    else:
        message.append(temp)
    # print(message)
message = "\n".join(message)
print(message)