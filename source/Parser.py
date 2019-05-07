from xml.dom import minidom
import os.path
from source.Validator import Validator
import collections
import json
import xml.parsers.expat


class Parser:
    def __init__(self, filename, result_filename="result.json"):
        self.filename = filename
        self.result_filename = result_filename
        self.validator = Validator()
        self.objects = []
        self.parsed = collections.OrderedDict()
        self.current_obj = None
        self.current_field = None

    def _load_file(self):
        if not os.path.isfile(self.filename):
            raise Exception("Error: File {} not found".format(self.filename))
        try:
            self.dom_document = minidom.parse(self.filename)
        except xml.parsers.expat.ExpatError as e:
            raise Exception("Error: File {}: {}".format(self.filename, str(e)))

    def get_objects(self):
        self.objects = self.dom_document.getElementsByTagName("object")
        self.validator.check_node_exists(self.objects, "object")

    @staticmethod
    def get_text(node_list):
        txt = []
        for node in node_list:
            if node.nodeType == node.TEXT_NODE:
                txt.append(node.data)
        return ''.join(txt)

    def process_objects(self):
        for i, obj in enumerate(self.objects):
            try:
                self.current_obj = i
                fields_dom = obj.getElementsByTagName("field")
                attributes = self.get_fields(fields_dom)
                obj_name_node = obj_name_node = obj.getElementsByTagName("obj_name")
                self.validator.check_node_exists(obj_name_node, "object[{}]".format(i))
                obj_name = self.get_text(obj_name_node[0].childNodes)
                self.validator.check_object_unique(obj_name, self.parsed, i)
                self.validator.check_attributes_count(obj_name, attributes, i)
                self.parsed[obj_name] = attributes
            except Exception as e:
                print(e)

    def get_fields(self, fields):
        attributes = collections.OrderedDict()
        for i, field in enumerate(fields):
            try:
                self.current_field = i
                field_name = self.get_field_attribute(field, "name")
                field_value = self.get_field_attribute(field, "value")
                field_type = self.get_field_attribute(field, "type")
                self.validator.validate_field_type(
                    field_type, "object[{}]_field_{}".format(self.current_obj, field_type)
                )
                if field_type == "int":
                    field_value = int(field_value)
                attributes[field_name] = field_value
            except Exception as e:
                print(e)
        return attributes

    def get_field_attribute(self, field, name):
        node = field.getElementsByTagName(name)
        location = "object[{}]_field[{}]_{}".format(self.current_obj, self.current_field, name)
        self.validator.check_node_exists(node, location)
        text = self.get_text(node[0].childNodes)
        self.validator.validate_string(text, location)
        return text

    def save_as_json(self):
        with open(self.result_filename, "w+") as file:
            json.dump(self.parsed, file)

    def parse(self):
        try:
            self._load_file()
            self.get_objects()
            self.process_objects()
            self.save_as_json()
        except Exception as e:
            print(e)


