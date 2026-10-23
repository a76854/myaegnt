from myagent.tools.toolRegistry import TOOL_CLASSES, tools


def test_registry_exposes_all_tools_without_instantiation():
    specs = tools()

    assert {s["function"]["name"] for s in specs} == {"bash", "context7", "web_search"}
    for spec in specs:
        assert spec["type"] == "function"
        function = spec["function"]
        assert function["description"]
        assert function["parameters"]["type"] == "object"
        assert "properties" in function["parameters"]


def test_tool_names_match_class_attributes():
    for cls in TOOL_CLASSES:
        assert cls.name
        assert cls.description
        assert cls.schema["type"] == "object"


def test_tool_names_are_unique():
    names = [cls.name for cls in TOOL_CLASSES]
    assert len(names) == len(set(names))


def test_tool_names_are_valid_function_names():
    import re

    for cls in TOOL_CLASSES:
        assert re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", cls.name), cls.name