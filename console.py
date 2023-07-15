#!/usr/bin/python3
"""HBNBCommand Module"""
import cmd
import re
import json
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """Class for the command interpreter."""
    prompt = "(hbnb) "

    def do_EOF(self, line):
        """
        Handles the End Of File (EOF) character.

        Args:
            line (str): The command line string.

        Returns:
            bool: True to exit the program.

        """
        print()
        return True

    def do_create(self, line):
        """
        Creates an instance of a class.

        Args:
            line (str): The command line string.

        """
        if not line:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            instance = storage.classes()[line]()
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """
        Prints the string representation of an instance.

        Args:
            line (str): The command line string.

        """
        if not line:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = f"{words[0]}.{words[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_quit(self, line):
        """
        Exits the program.

        Args:
            line (str): The command line string.

        Returns:
            bool: True to exit the program.

        """
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER."""
        pass

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and ID.

        Args:
            line (str): The command line string.

        """
        if not line:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = f"{words[0]}.{words[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """
        Prints the string representation of instances

        Args:
            line (str): The command line string.

        """
        if line:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                instance_list = [str(obj) for key, obj in storage.all().items()
                                 if type(obj).__name__ == words[0]]
                print(instance_list)
        else:
            instance_list = [str(obj) for key, obj in storage.all().items()]
            print(instance_list)

    def do_count(self, line):
        """
        Counts the instances of a class.

        Args:
            line (str): The command line string.

        """
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))

    def do_update(self, line):
        """
        Updates an instance by adding or updating an attribute.

        Args:
            line (str): The command line string.

        """
        if not line:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        class_name = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = f"{class_name}.{uid}"
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[class_name]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def default(self, line):
        """Called when the entered command is not recognized."""
        self.preprocess_command(line)

    def preprocess_command(self, line):
        """
        Preprocesses the command entered by the user.

        Args:
            line (str): The command entered by the user.

        Returns:
            str: The processed command.

        """
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line

        class_name, method, args = match.group(
            1), match.group(2), match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)

        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_instance_dict(class_name, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")

        command = f"{method} {class_name} {uid} {attr_and_value}"
        self.onecmd(command)
        return command

    def update_instance_dict(self, class_name, uid, s_dict):
        """
        Updates an instance with values from a dictionary.

        Args:
            class_name (str): The name of the class.
            uid (str): The ID of the instance.
            s_dict (str): The dictionary representation of the attributes.

        """
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not class_name:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = f"{class_name}.{uid}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[class_name]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
