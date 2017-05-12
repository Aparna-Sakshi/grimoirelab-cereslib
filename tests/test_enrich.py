# Copyright (C) 2016 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Daniel Izquierdo <dizquierdo@bitergia.com>
#     Alberto Perez <alpgarcia@bitergia.com>
#

import sys

import unittest

import pandas

import scipy

if not '..' in sys.path:
    sys.path.insert(0, '..')

from enrich import PairProgramming, TimeDifference, Uuid

from format import Format

class TestEnrich(unittest.TestCase):
    """ Unit tests for Enrich classes
    """

    def test_PairProgramming(self):
        """ Test several cases for the PairProgramming class
        """

        empty_df = pandas.DataFrame()
        # With empty dataframe and any columns, this always returns empty dataframe
        # A DataFrame with columns but not data is an empty DataFrame
        pair = PairProgramming(empty_df)
        self.assertTrue(pair.enrich("test1","test2").empty)
        # With a dataframe with some data, this returns a non-empty dataframe

        csv_df = pandas.read_csv("data/enrich/pairprogramming.csv")
        pair = PairProgramming(csv_df)
        enriched_df = pair.enrich("test1","test2")
        self.assertFalse(enriched_df.empty)
        # Expected to return the same df as test1 and test2 do not exist
        self.assertEqual(len(enriched_df), 7)

        enriched_df = pair.enrich("author", "committer")
        self.assertFalse(enriched_df.empty)
        # Expected to add a new entry at the end of the dataframe
        self.assertEqual(len(enriched_df), 8)

        enriched_df = pair.enrich("committer", "author")
        self.assertFalse(enriched_df.empty)
        # Expected to add a new entry at the end of the dataframe
        self.assertEqual(len(enriched_df), 8)


    def test_TimeDifference(self):
        """ Several test cases for the TimeDifference class
        """

        empty_df = pandas.DataFrame()
        # With empty dataframe and any columns this always returns emtpy datafram
        # A DataFrame with columns but no data is an empty DataFrame
        time = TimeDifference(empty_df)
        self.assertTrue(time.enrich("fake_column1", "fake_column2").empty)

        # A dataframe with some data, this returns a non-empty dataframe
        csv_df = pandas.read_csv("data/enrich/timedifference.csv")
        time = TimeDifference(csv_df)
        format_ = Format()
        time.data = format_.format_dates(time.data, ["date_author", "date_committer"])

        enriched_df = time.enrich("fake_column1", "fake_column2")
        self.assertFalse(enriched_df.empty)
        # Expected to return the same df as fake columns do not exist
        self.assertEqual(len(enriched_df), 7)

        enriched_df = time.enrich("date_author", "date_committer")

        self.assertEqual(len(enriched_df[enriched_df["timedifference"] > 0]), 4)


    def test_Uuid(self):
        """ Test several cases for the Uuid class
        """

        # Empty LEFT dataframe
        empty_df = pandas.DataFrame()
        uuid = Uuid(empty_df, file_path='data/enrich/uuids.csv')

        enriched_df = uuid.enrich(['name', 'email'])

        # If LEFT df is empty, nothing should be merged resulting in an empty df
        self.assertTrue(enriched_df.empty)

        # Load test data from CSV files
        authors_df = pandas.read_csv("data/enrich/authors.csv")
        uuid = Uuid(authors_df, file_path='data/enrich/uuids.csv')

        enriched_df = uuid.enrich(['name', 'email'])

        self.assertFalse(enriched_df.empty)
        # Merged len must be equal to LEFT df len
        self.assertEqual(len(enriched_df), len(authors_df))

        # Check rows that should store same uuid, i.e., same author
        self.assertEqual(len(enriched_df[enriched_df['name'] == 'pepe']), 2)
        self.assertEqual(len(enriched_df[enriched_df['name'] == 'John Rambo']), 3)

        pepe_df = enriched_df[enriched_df['name'] == 'pepe']
        pepe_uuid = '0007b2fd4dbb5090a848c50717966a15a1772112'
        self.assertEqual(pepe_df.iloc[[0]]['uuid'].item(), pepe_uuid)
        self.assertEqual(pepe_df.iloc[[1]]['uuid'].item(), pepe_uuid)

        john_df = enriched_df[enriched_df['name'] == 'John Rambo']
        john_uuid = '000eabca391efd736dd8438e4d220b3f00808065'
        self.assertEqual(john_df.iloc[[0]]['uuid'].item(), john_uuid)
        self.assertEqual(john_df.iloc[[1]]['uuid'].item(), john_uuid)
        self.assertEqual(john_df.iloc[[2]]['uuid'].item(), john_uuid)


if __name__ == '__main__':
    unittest.main()
