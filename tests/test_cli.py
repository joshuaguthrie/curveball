#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of curveball.
# https://github.com/yoavram/curveball

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Yoav Ram <yoav@yoavram.com>
from unittest import TestCase, main
from nose.plugins.skip import SkipTest
import os
import glob
import io
import shutil
import pkg_resources
import pandas as pd
from click.testing import CliRunner # See reference on testing Click applications: http://click.pocoo.org/5/testing/
from curveball.scripts import cli
import curveball


CI = os.environ.get('CI', 'false').lower() == 'true'


def is_csv(data):
	lines = data.splitlines()
	data  = map(lambda line: line.split(','), lines)
	lengths = map(len, data)
	return all(x==lengths[0] for x in lengths)


class SimpleTestCase(TestCase):
	_multiprocess_can_split_ = True

	def setUp(self):
		self.runner = CliRunner()


	def tearDown(self):
		pass


	def test_help(self):
		result = self.runner.invoke(cli.cli, ['--help'])
		self.assertEquals(result.exit_code, 0)


	def test_version(self):
		result = self.runner.invoke(cli.cli, ['--version'])
		self.assertEquals(result.exit_code, 0)
		self.assertIn(curveball.__version__, result.output)


class PlateTestCase(TestCase):
	_multiprocess_can_split_ = True


	def setUp(self):
		self.runner = CliRunner()


	def _is_plate_csv(self, data):
		self.assertTrue(is_csv(data))
		newlines = data.count("\n")
		self.assertEquals(newlines, 97) # 96 wells, 1 header line


	def test_default_plate(self):
		result = self.runner.invoke(cli.cli, ['plate'])
		self.assertEquals(result.exit_code, 0)
		self._is_plate_csv(result.output)


	def test_non_default_plate(self):
		result = self.runner.invoke(cli.cli, ['plate', '--plate_file=G-RG-R.csv'])
		self.assertEquals(result.exit_code, 0)
		self._is_plate_csv(result.output)


	def test_default_plate_to_file(self):
		filename = 'plate.csv'
		with self.runner.isolated_filesystem():
			result = self.runner.invoke(cli.cli, ['plate', '--output_file={0}'.format(filename)])
			self.assertEquals(result.exit_code, 0)
			with open(filename, 'r') as f:
				data = f.read()		
			self._is_plate_csv(data)


class AnalysisTestCase(TestCase):
	_multiprocess_can_split_ = True


	def setup_with_context_manager(self, cm):
	    """Use a contextmanager to setUp a test case.
	    See http://nedbatchelder.com/blog/201508/using_context_managers_in_test_setup.html
	    """
	    val = cm.__enter__()
	    self.addCleanup(cm.__exit__, None, None, None)
	    return 


	def setUp(self):
		self.files = pkg_resources.resource_listdir('data', '')
		self.files = filter(lambda fn: os.path.splitext(fn)[-1] in ['.xlsx', '.mat'], self.files)
		self.runner = CliRunner()
		self.ctx = self.setup_with_context_manager(self.runner.isolated_filesystem())
		self.dirpath = os.getcwd()
		self.assertTrue(os.path.exists(self.dirpath))
		self.assertTrue(os.path.isdir(self.dirpath))

		for fn in self.files:
			src = pkg_resources.resource_filename('data', fn)
			shutil.copy(src, '.')
			self.assertTrue(os.path.exists(os.path.join(self.dirpath, fn)))
			self.assertTrue(os.path.isfile(os.path.join(self.dirpath, fn)))
		self.filepath = os.path.join(self.dirpath, self.files[0])
		

	def tearDown(self):
		pass	


	def test_process_file(self):
		result = self.runner.invoke(cli.cli, ['--no-plot', '--no-verbose', '--no-prompt', 'analyse', self.filepath, '--plate_file=G-RG-R.csv', '--ref_strain=G'])
		self.assertEquals(result.exit_code, 0, result.output)		
		lines = filter(lambda line: len(line) > 0, result.output.splitlines()) 
		data = os.linesep.join(lines[-4:]) # only last 4 lines
		self.assertTrue(is_csv(data))


	def test_process_file2(self):
		filepath = os.path.join(self.dirpath, self.files[1])
		result = self.runner.invoke(cli.cli, ['--no-plot', '--no-verbose', '--no-prompt', 'analyse', filepath, '--plate_file=G-RG-R.csv', '--ref_strain=G'])
		self.assertEquals(result.exit_code, 0, result.output)		
		lines = filter(lambda line: len(line) > 0, result.output.splitlines()) 
		data = os.linesep.join(lines[-4:]) # only last 4 lines
		self.assertTrue(is_csv(data))


	def test_process_file_to_file(self):
		result = self.runner.invoke(cli.cli, ['--no-plot', '--no-verbose', '--no-prompt', 'analyse', self.filepath, '--plate_file=G-RG-R.csv', '--ref_strain=G', '--output_file=summary.csv'])
		self.assertEquals(result.exit_code, 0, result.output)		
		with open('summary.csv', 'r') as f:
			data = f.read()
		self.assertTrue(is_csv(data))

	# FIXME - fails on CI, succeeds on local
	# def test_create_plots(self):
	# 	result = self.runner.invoke(cli.cli, ['--plot', '--verbose', '--no-prompt', 'analyse', self.filepath, '--plate_file=G-RG-R.csv', '--ref_strain=G'])
	# 	self.assertEquals(result.exit_code, 0, result.output)
	# 	path,ext = os.path.splitext(self.filepath)		
	# 	plot_files = glob.glob(path + "_*.png")
	# 	self.assertNotEqual(len(plot_files), 0, result.output)


	def test_process_dir(self):
		result = self.runner.invoke(cli.cli, ['--no-plot', '--verbose', '--no-prompt', 'analyse', self.dirpath, '--plate_file=G-RG-R.csv', '--ref_strain=G'])
		self.assertEquals(result.exit_code, 0, result.output)		
		lines = filter(lambda line: len(line) > 0, result.output.splitlines()) 
		num_lines = len(self.files) * 3 + 1
		data = os.linesep.join(lines[-num_lines:])
		self.assertTrue(is_csv(data), result.output)
		

if __name__ == '__main__':
    main()
