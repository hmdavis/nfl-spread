import csv
import math

def run():
  years = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013']
  weeks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
  counts = {}
  totals = {}
  corrects = {}

  opened_file = open('output.csv')
  csv_data = csv.reader(opened_file, delimiter=',')
  total = 0.0
  correct = 0.0
  count = 0
  for row in csv_data:
    if row[3] in years:

      if row[0] not in counts:
        counts[row[0]] = 0.0
      if row[0] not in totals:
        totals[row[0]] = 0.0
      if row[0] not in corrects:
        corrects[row[0]] = 0.0

      line = float(row[1])
      actual = float(row[2])
      margin = math.fabs(line - actual)
      if (line > 0 and actual > 0) or (line < 0 and actual < 0):
        corrects[row[0]] = corrects[row[0]] + 1
        correct = correct + 1
      totals[row[0]] = totals[row[0]] + margin
      total = total + margin
      counts[row[0]] = counts[row[0]] + 1
      count = count + 1

  for t in totals:
    print "Week: " + str(t)
    print "Margin: " + str(totals[t] / counts[t])
    print "Winner: " + str(corrects[t] / counts[t])
  print "Margin"
  print total / count
  print "Winner"
  print correct / count

if __name__ =='__main__':
  run()
