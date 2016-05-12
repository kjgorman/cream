def load_example():
    with open("squished.csv", "r") as fd:
        return fd.readlines()

def process_example():
    lines = load_example()
    headers = lines[0]
    content = lines[1:]

    rows = map(lambda l: l.replace("\n","").split(","), content)

    squashed = []
    currentDay     = None
    currentBalance = 0

    for row in rows:
        day = row[0]
        balance = row[1]
        if day == currentDay:
            currentBalance += balance
        else:
            squashed.append([ currentDay, currentBalance ])
        currentDay = day
        currentBalance = balance

    return squashed[1:]

def transpose(rows):
    xs = []
    ys = []

    for row in rows:
        xs.append(row[0])
        ys.append(row[1])

    return xs, ys
