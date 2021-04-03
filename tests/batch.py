import unittest
import csv
import hedy

class TestsBatch(unittest.TestCase):

  def test_bad_input(self):
    with open('batch_tests/2-logs-plain.csv', newline='', encoding='utf-8-sig') as csvfile:
      reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
      columns = reader.fieldnames

      csv_file_out = open("batch_tests/still_error.csv", "w+")
      writer = csv.DictWriter(csv_file_out, fieldnames=columns)
      writer.writeheader()

      for row in reader:
        code = row['code']
        level = row['level']
        try:
          hedy.transpile(code, level)
        except Exception as E:
          writer.writerow(row)


    csv_file_out.close()