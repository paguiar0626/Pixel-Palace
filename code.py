fname = input()

def decode(message_file):
    place= [] #numbers in the first column of the text file
    words = [] #words in the second column
    f = open(message_file, "r")
    lines = f.readlines()
    for i in lines:
        place.append(i.split(' ')[0])
        words.append(i.split(' ')[-1])
    n = 1 #keeps track of the next number that will be appended to the pyramid
    pyramid = []
    while (n < len(place)):
        n = get_pyramid_values(n, len(pyramid) + 1) #depth of pyramid + 1
        pyramid.append(n)

    message = []
    place.index(1)
    for i in range(len(pyramid)):
        word_idx = place.index(pyramid[i]) #index of the next word to be added
        message.append(words[word_idx])

    ans = " "
    return (ans.join(message))
        
def get_pyramid_values (n, i):
    index = 0
    if (n == 1 and i == 1):
        index = 1
    else:
        index = n + i
    return index



decode(fname)
