import csv

with open('footprint.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    var = 0
    for row in csv_reader:
        if line_count > 1000:
            break
        if line_count == 0:
            # print(Error: No Food Items Found)
            pass
        else:
            foodName = row[1]
            waterFootprint = float(row[2])+float(row[3])+float(row[4])
            carbonFootprint = float(row[7])+float(row[8])+float(row[9])

            foodInfo = [foodName.lower(), round(
                waterFootprint, 5), round(carbonFootprint, 5)]
            print(foodInfo)
        line_count += 1
