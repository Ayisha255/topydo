# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import CommandTest
import DepCommand
import TodoList

class DepCommandTest(CommandTest.CommandTest):
    def setUp(self):
        todos = [
            "Foo id:1",
            "Bar p:1",
            "Baz p:1",
            "Fnord id:2",
            "Garbage dependency p:99",
            "Fart p:2",
        ]

        self.todolist = TodoList.TodoList(todos)

    def test_add1(self):
        command = DepCommand.DepCommand(["add", "1", "to", "4"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "")

    def test_add2(self):
        command = DepCommand.DepCommand(["add", "1", "4"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "")

    def test_add3(self):
        command = DepCommand.DepCommand(["add", "99", "3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_add4(self):
        command = DepCommand.DepCommand(["add", "A", "3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_add5(self):
        command = DepCommand.DepCommand(["add", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n")
    def rm_helper(self, p_args):
        """
        Helper function that checks the removal of the dependency from todo 1
        to todo 3.
        """

        command = DepCommand.DepCommand(p_args, self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(1).has_tag('id', '1'))
        self.assertFalse(self.todolist.todo(3).has_tag('p', '1'))
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "")

    def test_rm1(self):
        self.rm_helper(["rm", "1", "to", "3"])

    def test_rm2(self):
        self.rm_helper(["rm", "1", "3"]) 

    def test_del1(self):
        self.rm_helper(["del", "1", "to", "3"])

    def test_del2(self):
        self.rm_helper(["del", "1", "3"]) 

    def test_rm3(self):
        command = DepCommand.DepCommand(["rm", "99", "3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_rm4(self):
        command = DepCommand.DepCommand(["rm", "A", "3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_rm5(self):
        command = DepCommand.DepCommand(["rm", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_ls1(self):
        command = DepCommand.DepCommand(["ls", "1", "to"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "  2 Bar p:1\n  3 Baz p:1\n")
        self.assertEquals(self.errors, "")

    def test_ls2(self):
        command = DepCommand.DepCommand(["ls", "99", "to"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_ls3(self):
        command = DepCommand.DepCommand(["ls", "to", "3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "  1 Foo id:1\n")
        self.assertEquals(self.errors, "")

    def test_ls4(self):
        command = DepCommand.DepCommand(["ls", "to", "99"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_ls5(self):
        command = DepCommand.DepCommand(["ls", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_ls6(self):
        command = DepCommand.DepCommand(["ls"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def gc_helper(self, p_subcommand):
        command = DepCommand.DepCommand([p_subcommand], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertFalse(self.errors)
        self.assertFalse(self.todolist.todo(5).has_tag('p', '99'))

    def test_clean(self):
        self.gc_helper("clean")

    def test_gc(self):
        self.gc_helper("gc")

    def test_invalid_subsubcommand(self):
        command = DepCommand.DepCommand(["foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")
        self.assertFalse(self.todolist.is_dirty())

    def test_no_subsubcommand(self):
        command = DepCommand.DepCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")
        self.assertFalse(self.todolist.is_dirty())

