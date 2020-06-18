import unittest
import os
from rocrate.rocrate import ROCrate
from rocrate.model.file import File
from rocrate.model.person import Person
from test.test_common import BaseTest
import tempfile
import pathlib
import zipfile
import shutil

class TestAPI(BaseTest):

    def test_file_writing(self):
        crate = ROCrate()

        # dereference added files
        sample_file = os.path.join(self.test_data_dir, 'sample_file.txt')
        file_returned = crate.add_file(sample_file)
        file_returned_subdir = crate.add_file(sample_file, 'subdir/sample_file2.csv')
        test_dir_path = os.path.join(self.test_data_dir,'test_add_dir')
        test_dir_entity = crate.add_directory(test_dir_path, 'test_add_dir')
        out_path = os.path.join(tempfile.gettempdir(),'ro_crate_out')
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        crate.write_crate(out_path)

        metadata_path = pathlib.Path(os.path.join(out_path, 'ro-crate-metadata.jsonld'))
        self.assertTrue(metadata_path.exists())
        file1 = pathlib.Path(os.path.join(out_path, 'sample_file.txt'))
        file2 = pathlib.Path(os.path.join(out_path, 'subdir','sample_file2.csv'))
        file_subdir = pathlib.Path(os.path.join(out_path, 'test_add_dir','sample_file_subdir.txt'))
        self.assertTrue(file1.exists())
        self.assertTrue(file2.exists())
        self.assertTrue(file_subdir.exists())


    def test_write_zip(self):
        crate = ROCrate()

        # dereference added files
        sample_file = os.path.join(self.test_data_dir, 'sample_file.txt')
        file_returned = crate.add_file(sample_file)
        file_returned_subdir = crate.add_file(sample_file, 'subdir/sample_file2.csv')
        test_dir_path = os.path.join(self.test_data_dir,'test_add_dir')
        test_dir_entity = crate.add_directory(test_dir_path, 'test_add_dir')

        #write to zip
        zip_path = tempfile.NamedTemporaryFile(suffix='.zip')
        crate.write_zip(zip_path.name)
        read_zip = zipfile.ZipFile(zip_path, mode='r')
        self.assertEqual(read_zip.getinfo('sample_file.txt').file_size, 12)
        self.assertEqual(read_zip.getinfo('test_add_dir/sample_file_subdir.txt').file_size, 18)
        self.assertEqual(read_zip.getinfo('sample_file_subdir.txt').file_size, 18)