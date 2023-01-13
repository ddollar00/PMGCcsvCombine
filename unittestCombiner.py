import pandas as pd
import sys
import generatefixtures
import unittest
import os
from csv_combiner import csvCombine
from io import StringIO


class TestCombineMethod(unittest.TestCase):

    
    test_output_path = "./test_output.csv"
    accessories = "./test_fix/accessories.csv"
    clothing = "./test_fix/clothing.csv"
    houseclean = "./test_fix/household_cleaners.csv"
    empty = "./test_fix/empty_file.csv"
    csv_c_path = "./csv_combiner.py"

    
    backup = sys.stdout
    test_output = open(test_output_path, 'w+')
    combiner = csvCombine()

    @classmethod
    def setUpClass(cls):
        generatefixtures.main()

        sys.stdout = cls.test_output

    def setUp(self):
        
        self.output = StringIO()
        sys.stdout = self.output
        self.test_output = open(self.test_output_path, 'w+')
        
    def breakd(self):
        self.test_output.close()
        self.test_output = open(self.test_output_path, 'w+')
        sys.stdout = self.backup
        self.test_output.truncate(0)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()
    
    def test_noFilesEntered(self):

        
        argv = [self.csv_c_path]
        self.combiner.combine(argv)

        self.assertIn("Enter a file path", self.output.getvalue())

    def test_emptyfile(self):

        
        argv = [self.csv_c_path, self.empty]
        self.combiner.combine(argv)

        self.assertIn("empty file: ", self.output.getvalue())

    def test_no_file(self):

       
        argv = [self.csv_c_path, "fakefil.csv"]
        self.combiner.combine(argv)

        self.assertTrue("couldn't find this File: " in self.output.getvalue())

    def test_filename_column(self):

    
        argv = [self.csv_c_path, self.accessories, self.clothing]
        self.combiner.combine(argv)

     
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        with open(self.test_output_path) as f:
            df = pd.read_csv(f)
        self.assertIn('filename', df.columns.values)

    def test_name_added_to_rows(self):
        argv = [self.csv_c_path, self.accessories, self.clothing]
        self.combiner.combine(argv)

        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        with open(self.test_output_path) as f:
            df = pd.read_csv(filepath_or_buffer=f, lineterminator='\n')
        self.assertIn('accessories.csv', df['filename'].tolist())
        

    def test_combined(self):

        argv = [self.csv_c_path, self.accessories, self.clothing,
                self.houseclean]
        self.combiner.combine(argv)
        
        self.test_output.write(self.output.getvalue())
        self.test_output.close()


        acc_df = pd.read_csv(filepath_or_buffer=self.accessories, lineterminator='\n')
        clo_df = pd.read_csv(filepath_or_buffer=self.clothing, lineterminator='\n')
        hc_df = pd.read_csv(filepath_or_buffer=self.houseclean, lineterminator='\n')
        

        with open(self.test_output_path) as f:
            combined_df = pd.read_csv(filepath_or_buffer=f, lineterminator='\n')
            self.assertEqual(len(combined_df.merge(hc_df)), len(combined_df.drop_duplicates()))
            
