class Validator:
    @staticmethod
    def check_node_exists(node, location):
        if not node:
            raise Exception("tag {} does not exist or is empty.".format(location))

    @staticmethod
    def validate_field_type(t, location):
        if t != "string" and t != "int":
            raise Exception("{} is not supported field type[{}], ignoring in".format(t, location))

    @staticmethod
    def validate_string(string, location):
        if not string.isprintable():
            raise Exception("string is not printable [{}], ignoring".format(location))
        if string == "":
            raise Exception("string is empty[{}]".format(location))

    @staticmethod
    def check_object_unique(object_name, objects, object_num):
        if object_name in objects:
            raise Exception("{} is not unique [in object[{}]".format(object_name, object_num))

    @staticmethod
    def check_attributes_count(object_name, attributes, object_num):
        if not attributes:
            raise Exception("Object: {} has no attributes [in object[{}]], ignoring".format(object_name, object_num))
