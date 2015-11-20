import textwrap

def join_lines(function):
    def wrapper(*args, **kwargs):
        return "\n".join(list(function(*args, **kwargs)))
    return wrapper

def indent(lines, indentation = 4):
    prefix = " " * indentation
    if isinstance(lines, str): lines = lines.split("\n")
    return [prefix + line for line in lines]

@join_lines
def make_operator_description(operator, width = 70):
    rna = operator.get_rna().bl_rna
    yield rna.name
    yield ""
    yield from textwrap.wrap(rna.description, width)
    yield ""

    parameters = [prop for prop in rna.properties if prop.identifier != "rna_type"]
    if len(parameters) == 0: return

    yield "Parameters:"
    for parameter in parameters:
        yield from indent(make_property_description(parameter, width - 3), indentation = 3)

@join_lines
def make_property_description(property, width = 70):
    identifier = "{}: ({})".format(property.identifier, get_readable_property_type(property))
    description = property.description

    if len(identifier + description) + 2 > width:
        yield identifier
        yield from indent(textwrap.wrap(description, width - 3), indentation = 3)
    else:
        yield "{} {}".format(identifier, description)

def get_readable_property_type(property):
    suffix = "[{}]".format(property.array_length) if getattr(property, "array_length", 1) > 1 else ""
    if property.type == "BOOLEAN": return "Boolean" + suffix
    if property.type == "INT": return "Integer" + suffix
    if property.type == "STRING": return "String" + suffix
    if property.type == "COLLECTION": return "Sequence of " + property.fixed_type.identifier
    if property.type == "FLOAT":
        if property.array_length <= 1: return "Float"
        if property.array_length == 2: return "Vector 2D"
        if property.array_length == 3: return "Vector 3D"
        if property.array_length == 16: return "Matrix"
        return "Float[{}]".format(property.array_length)
    if property.type == "POINTER": return property.fixed_type.identifier
    if property.type == "ENUM": return "Enum"