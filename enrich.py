#!/usr/bin/python
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
#   Daniel Izquierdo Cortazar <dizquierdo@bitergia.com>
#


import pandas

class Enrich(object):
    """ Class that enriches information for a given dataset.

    Its usual way of working consists of providing a new columns
    in the dataframe from a given entry. This allows to keep
    adding extra information to the basics coming from the original
    data source.

    An example of this would be the addition of the affiliation,
    gender, workload adequacy and other metrics for a given commmit.
    """


class PairProgramming(Enrich):
    """ This class splits a commit into 2 of them according to the author name.

    There are cases where two developers have participated in a commit.
    One of the ways to identify those is claiming that commit as author, but
    also as a committer.

    Depending on the process of the organization, this may indicate a review
    process, a peer development process or even nothing.

    This class should be called when committer an author usually participate
    in the development of such commit.
    """

    def __init__(self, commits):
        """ Main constructor of the class

        :param commits: original list of commits
        :type commits: dataframe with commit information
        """

        self.commits = commits

    def enrich(self, column1, column2):
        """ This class splits those commits where column1 and column2
        values are different

        :param column1: column to compare to column2
        :param column2: column to compare to column1
        :type column1: string
        :type column2: string

        :returns: self.commits with duplicated rows where the values at
            columns are different. The original row remains while the second
            row contains in column1 and 2 the value of column2.
        :rtype: pandas.DataFrame
        """

        if column1 not in self.commits.columns or \
           column2 not in self.commits.columns:
            return self.commits

        # Select rows where values in column1 are different from
        # values in column2
        pair_df = self.commits[self.commits[column1]<>self.commits[column2]]
        new_values = list(pair_df[column2])
        # Update values from column2
        pair_df[column1] = new_values

        # This adds at the end of the original dataframe those rows duplicating
        # information and updating the values in column1
        return self.commits.append(pair_df)

