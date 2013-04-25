# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# BitBake Tests for the pysh lexer (pysh/)
#
# Copyright (C) 2013 Olof Johansson <olof.johansson@axis.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import unittest
from bb.pysh.pyshlex import WordLexer, NeedMore

orig_init = WordLexer.__init__

class WordLexerParseTest(unittest.TestCase):
    # mock out WordLexer's constructor
    def SetUp(self):
        WordLexer.__init__ = lambda: None

    def TearDown(self):
        WordLexer.__init__ = orig_init

    # The arithmetic tests make sure that WordLexer's _parse_arithmetic
    # method can parse out the expected shell arithmetic expression,
    # including support for nested expressions.
    def assertArithmeticParser(self, expr, expect=None, eof=True, length=None):
        expr = expr[3:] # strip off $((
        result = ["$((", ""]
        buf = list(expr)

        # Unless stated otherwise, let's assume the complete buf
        # is an shell arithmetic expression.
        if not expect:
            expect = ["$((", expr[:-2], "))"]
        if not length:
            length = len(expr)

        wl = WordLexer()
        pos, got_eof = WordLexer._parse_arithmetic(wl, buf, result, True)

        self.assertEqual(buf, list(expr))
        self.assertEqual(result, expect)
        self.assertEqual(pos, length)
        self.assertEqual(got_eof, eof)

    def test_parse_arithmetic_simple(self):
        self.assertArithmeticParser("$((1+1))")

    def test_parse_arithmetic_simple_trailing(self):
        self.assertArithmeticParser(
            "$((1+1)); uptime",
            expect=["$((", "1+1", "))"],
            length=5,
            eof=False)

    def test_parse_arithmetic_incomplete(self):
        wl = WordLexer()
        res = ["$((", ""]
        buf = list("10+")

        needs_more = False
        try:
            pos, got_eof = WordLexer._parse_arithmetic(wl, buf, res, True)
        except NeedMore:
            needs_more = True

        self.assertTrue(needs_more)

    def test_parse_arithmetic_empty(self):
        wl = WordLexer()
        res = ["$((", ""]
        buf = list("")

        needs_more = False
        try:
            pos, got_eof = WordLexer._parse_arithmetic(wl, buf, res, True)
        except NeedMore:
            needs_more = True

        self.assertTrue(needs_more)

    def test_parse_arithmetic_simple_whitespace(self):
        self.assertArithmeticParser("$(( 1 + 1 ))")

    def test_parse_arithmetic_nested1(self):
        self.assertArithmeticParser("$((1+$((1+2))))")

    def test_parse_arithmetic_nested2(self):
        self.assertArithmeticParser("$(($((1+2))+$((1+2))))")

    def assertCommandParser(self, command="", sep=("$(", ")"), eof=True):
        result = [sep[0], ""]
        buf = ''.join([command, sep[1]])

        wl = WordLexer()
        pos, got_eof = WordLexer._parse_command(wl, buf, result, True)

        self.assertEqual(result, [sep[0], command, sep[1]])

    def test_parse_command_simple(self):
        self.assertCommandParser("uptime")

    def test_parse_command_backticks(self):
        self.assertCommandParser("echo bar", sep=("`", "`"))

    #def test_parse_command_nested(self):
    #    self.assertCommandParser("echo $(uptime)")
