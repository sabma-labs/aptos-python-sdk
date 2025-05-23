import typing

import six
from _typeshed import Incomplete
from behave.matchers import NoMatch as NoMatch
from behave.model_core import BasicStatement as BasicStatement
from behave.model_core import Replayable as Replayable
from behave.model_core import Status as Status
from behave.model_core import TagAndStatusStatement as TagAndStatusStatement
from behave.model_core import TagStatement as TagStatement

class Feature(TagAndStatusStatement, Replayable):
    type: str
    description: Incomplete
    scenarios: Incomplete
    background: Incomplete
    language: Incomplete
    parser: Incomplete
    hook_failed: bool
    def __init__(
        self,
        filename,
        line,
        keyword,
        name,
        tags: Incomplete | None = None,
        description: Incomplete | None = None,
        scenarios: Incomplete | None = None,
        background: Incomplete | None = None,
        language: Incomplete | None = None,
    ) -> None: ...
    def reset(self) -> None: ...
    def __iter__(self): ...
    def add_scenario(self, scenario) -> None: ...
    def compute_status(self): ...
    @property
    def duration(self): ...
    def walk_scenarios(self, with_outlines: bool = False): ...
    def should_run(self, config: Incomplete | None = None): ...
    def should_run_with_tags(self, tag_expression): ...
    def mark_skipped(self) -> None: ...
    should_skip: bool
    skip_reason: Incomplete
    def skip(
        self, reason: Incomplete | None = None, require_not_executed: bool = False
    ) -> None: ...
    def run(self, runner): ...

class Background(BasicStatement, Replayable):
    type: str
    steps: Incomplete
    def __init__(
        self, filename, line, keyword, name, steps: Incomplete | None = None
    ) -> None: ...
    def __iter__(self): ...
    @property
    def duration(self): ...

class Scenario(TagAndStatusStatement, Replayable):
    type: str
    continue_after_failed_step: bool
    description: Incomplete
    steps: Incomplete
    background: Incomplete
    feature: Incomplete
    hook_failed: bool
    was_dry_run: bool
    def __init__(
        self,
        filename,
        line,
        keyword,
        name,
        tags: Incomplete | None = None,
        steps: Incomplete | None = None,
        description: Incomplete | None = None,
    ) -> None: ...
    def reset(self) -> None: ...
    @property
    def background_steps(self): ...
    @property
    def all_steps(self): ...
    def __iter__(self): ...
    def compute_status(self): ...
    @property
    def duration(self): ...
    @property
    def effective_tags(self): ...
    def should_run(self, config: Incomplete | None = None): ...
    def should_run_with_tags(self, tag_expression): ...
    def should_run_with_name_select(self, config): ...
    def mark_skipped(self) -> None: ...
    should_skip: bool
    skip_reason: Incomplete
    def skip(
        self, reason: Incomplete | None = None, require_not_executed: bool = False
    ) -> None: ...
    captured: Incomplete
    def run(self, runner): ...

class ScenarioOutlineBuilder:
    annotation_schema: Incomplete
    def __init__(self, annotation_schema) -> None: ...
    @staticmethod
    def render_template(
        text, row: Incomplete | None = None, params: Incomplete | None = None
    ): ...
    name: Incomplete
    index: Incomplete
    id: Incomplete
    def make_scenario_name(
        self, outline_name, example, row, params: Incomplete | None = None
    ): ...
    @classmethod
    def make_row_tags(cls, outline_tags, row, params: Incomplete | None = None): ...
    @classmethod
    def make_step_for_row(cls, outline_step, row, params: Incomplete | None = None): ...
    def build_scenarios(self, scenario_outline): ...

class ScenarioOutline(Scenario):
    type: str
    annotation_schema: str
    examples: Incomplete
    def __init__(
        self,
        filename,
        line,
        keyword,
        name,
        tags: Incomplete | None = None,
        steps: Incomplete | None = None,
        examples: Incomplete | None = None,
        description: Incomplete | None = None,
    ) -> None: ...
    def reset(self) -> None: ...
    @property
    def scenarios(self): ...
    def __iter__(self): ...
    def compute_status(self): ...
    @property
    def duration(self): ...
    def should_run_with_tags(self, tag_expression): ...
    def should_run_with_name_select(self, config): ...
    def mark_skipped(self) -> None: ...
    should_skip: bool
    def skip(
        self, reason: Incomplete | None = None, require_not_executed: bool = False
    ) -> None: ...
    def run(self, runner): ...

class Examples(TagStatement, Replayable):
    type: str
    table: Incomplete
    index: Incomplete
    def __init__(
        self,
        filename,
        line,
        keyword,
        name,
        tags: Incomplete | None = None,
        table: Incomplete | None = None,
    ) -> None: ...

class Step(BasicStatement, Replayable):
    type: str
    step_type: Incomplete
    text: Incomplete
    table: Incomplete
    status: Incomplete
    hook_failed: bool
    duration: int
    def __init__(
        self,
        filename,
        line,
        keyword,
        step_type,
        name,
        text: Incomplete | None = None,
        table: Incomplete | None = None,
    ) -> None: ...
    def reset(self) -> None: ...
    def __eq__(self, other): ...
    def __hash__(self): ...
    def set_values(self, table_row): ...
    captured: Incomplete
    error_message: Incomplete
    def run(self, runner, quiet: bool = False, capture: bool = True): ...

class Table(Replayable):
    type: str
    headings: Incomplete
    line: Incomplete
    rows: Incomplete
    def __init__(
        self, headings, line: Incomplete | None = None, rows: Incomplete | None = None
    ) -> None: ...
    def add_row(self, row, line: Incomplete | None = None) -> None: ...
    def add_column(
        self, column_name, values: Incomplete | None = None, default_value: str = ""
    ): ...
    def remove_column(self, column_name) -> None: ...
    def remove_columns(self, column_names) -> None: ...
    def has_column(self, column_name): ...
    def get_column_index(self, column_name): ...
    def require_column(self, column_name): ...
    def require_columns(self, column_names) -> None: ...
    def ensure_column_exists(self, column_name): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __iter__(self): ...
    def __getitem__(self, index): ...
    def assert_equals(self, data) -> None: ...

class Row:
    headings: Incomplete
    comments: Incomplete
    cells: Incomplete
    line: Incomplete
    def __init__(
        self,
        headings,
        cells,
        line: Incomplete | None = None,
        comments: Incomplete | None = None,
    ) -> None: ...
    def __getitem__(self, name): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __len__(self) -> int: ...
    def __iter__(self): ...
    def items(self): ...
    def get(self, key, default: Incomplete | None = None): ...
    def as_dict(self): ...

class Tag(six.text_type):
    allowed_chars: str
    quoting_chars: Incomplete
    def __new__(cls, name, line): ...
    @classmethod
    def make_name(
        cls, text, unescape: bool = False, allowed_chars: Incomplete | None = None
    ): ...

class Text(six.text_type):
    def __new__(cls, value, content_type: str = "text/plain", line: int = 0): ...
    def line_range(self): ...
    def replace(self, old, new, SupportsIndex: typing.Any = -1): ...
    def assert_equals(self, expected): ...

def reset_model(model_elements) -> None: ...
