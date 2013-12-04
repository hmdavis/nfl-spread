import csv
import math

def run():
  years = ['2011','2012','2013']
  opened_file = open('output.csv')
  csv_data = csv.reader(opened_file, delimiter=',')
  total = 0.0
  correct = 0.0
  count = 0
  for row in csv_data:
    if row[3] in years:
      line = float(row[1])
      actual = float(row[2])
      margin = math.fabs(line - actual)
      if (line > 0 and actual > 0) or (line < 0 and actual < 0):
        correct = correct + 1
      else:
        print row
        print margin
      total = total + margin
      count = count + 1
  print "Margin"
  print total / count
  print "Winner"
  print correct / count

if __name__ =='__main__':
  run()
