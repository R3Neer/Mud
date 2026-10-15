"""Bounded metadata inventory and scenario planner for this example, not a Mud compiler.

Accept only its stored enum metadata, closed activation catalogue and literal
scenario setup template. Never execute Mud, resolve arbitrary programs or infer
calls through descriptor values. Unknown catalogue shapes fail explicitly.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tooling.cli_support import (HelpCatalogue, HelpItem, MudArgumentParser,
                                 add_presentation_arguments, failure, parse_cli)

EXAMPLE = ROOT / 'notes/examples/duelo-spellcasting'
HEAD = re.compile(r'^(?:(?:abstract|always) )?(family|alias|thing|rule|action|subaction|look|sublook|message|submessage|test) (\w+)', re.M)
MASK = re.compile(r'"(?:\\.|[^"\\])*"|\#[^\n]*')
NAME = r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*'


@dataclass(frozen=True)
class Declaration:
    name: str
    path: str
    category: str
    body: str
    defaults: str

    @property
    def qualified(self) -> str:
        return f'{self.path}.{self.name}' if self.path else self.name


def mask(source: str) -> str:
    return MASK.sub(lambda m: ''.join('\n' if c == '\n' else ' ' for c in m[0]), source)


def check_dictionary_arguments(source: str) -> None:
    """Catch the known byStage tuple/association-list mistake, not general typing."""
    for match in re.finditer(r'\bbyStage\s*=\s*\(', source):
        stack = ['(']
        for char in source[match.end():]:
            if char in '([{':
                stack.append(char)
            elif char in ')]}':
                if not stack or stack.pop() != {')': '(', ']': '[', '}': '{'}[char]:
                    raise ValueError('Unbalanced byStage grouping')
                if not stack:
                    break
            elif char == ',' and len(stack) == 1:
                raise ValueError('SpellFeedbackProfile.byStage requires dictionary associations in [...], not a tuple')
        if stack:
            raise ValueError('Unclosed byStage grouping')


def metadata(source: str, key: str, contract: str, prefix: str, many: bool) -> frozenset[str] | None:
    mentions = list(re.finditer(r'~' + key + r'\b', source))
    if not mentions:
        return None
    match = re.search(r'~' + key + r'\s*:\s*([^=\n]+)\s*=\s*(\[[^\]]*\]|' + NAME + r')', source)
    if len(mentions) != 1 or match is None:
        raise ValueError(f'{key}: expected one stored literal metadata entry')
    if re.sub(r'\s+', '', match[1]) != re.sub(r'\s+', '', contract):
        raise ValueError(f'{key}: incompatible contract {match[1].strip()}')
    tail = source[match.end():]
    if tail.split('\n', 1)[0].strip(' \t\r;,}'):
        raise ValueError(f'{key}: only a complete literal value is supported')
    if tail.lstrip().startswith(('|', '&', 'to ', 'in ', '[', '+')):
        raise ValueError(f'{key}: computed continuations are unsupported')
    value = match[2].strip()
    if many != value.startswith('['):
        raise ValueError(f'{key}: unexpected scalar/collection shape')
    values = value[1:-1].split(',') if many else [value]
    result = set()
    for item in values:
        item = item.strip()
        if not re.fullmatch(re.escape(prefix) + r'\.[A-Z]\w*', item):
            raise ValueError(f'{key}: unsupported enum value {item!r}')
        result.add(item.rsplit('.', 1)[1])
    if not result:
        raise ValueError(f'{key}: empty metadata is not admitted')
    return frozenset(result)


def effective(decl: Declaration, key: str, contract: str, prefix: str, many: bool) -> frozenset[str]:
    local = metadata(decl.body, key, contract, prefix, many)
    default = metadata(decl.defaults, key, contract, prefix, many)
    result = local if local is not None else default
    if result is None:
        raise ValueError(f'{decl.qualified}: missing {key}')
    return result


class Inventory:
    def __init__(self, root: Path):
        manifests = list(root.rglob('mud.part'))
        if manifests != [root / 'mud.part'] or mask(manifests[0].read_text()).strip():
            raise ValueError('This planner supports one comment-only root part, without foreign dependencies')
        self.declarations: dict[str, Declaration] = {}
        for file in sorted(root.rglob('*.mud')):
            source = mask(file.read_text(encoding='utf-8-sig'))
            check_dictionary_arguments(source)
            heads = list(HEAD.finditer(source))
            for index, head in enumerate(heads):
                end = heads[index + 1].start() if index + 1 < len(heads) else len(source)
                text = source[head.end():end]
                opening = text.find('{')
                body = text[opening + 1:text.rfind('}')] if opening >= 0 else ''
                path = '.'.join(file.relative_to(root).parts[:-1])
                decl = Declaration(head[2], path, head[1], body, source[:heads[0].start()])
                if decl.name in self.declarations:
                    raise ValueError(f'Ambiguous short name unsupported by this inventory: {decl.name}')
                self.declarations[decl.name] = decl
        self.features = self.enum('ActivationFeature')
        self.concerns = self.enum('TestConcern')
        self.modalities = self.enum('FeedbackModality')
        registry = re.sub(r'\s+', ' ', self.declarations['ActivationSelection'].body).strip()
        match = re.fullmatch(
            r'\s*let features:\s*ActivationFeature \[\* unique\] = empty\s*'
            r'let declarations := foreach declaration in \[([^\]]+)\]\s*'
            r'if\s*\(features \| \[ActivationFeature.Core\]\) has declaration~activationFeature --> declaration\s*', registry)
        if not match:
            raise ValueError('Unsupported activation catalogue/selection template')
        self.support = {}
        for name in match[1].split(','):
            decl = self.reference(name.strip())
            if decl.category not in {'thing', 'rule'}:
                raise ValueError(f'{decl.qualified}: not activatable support')
            if decl.qualified in self.support:
                raise ValueError(f'Duplicate activation registration: {decl.qualified}')
            feature = effective(decl, 'activationFeature', 'configuration.ActivationFeature', 'configuration.ActivationFeature', False)
            if not feature <= self.features:
                raise ValueError(f'{decl.qualified}: unknown activation feature')
            self.support[decl.qualified] = next(iter(feature))
        for decl in self.declarations.values():
            if decl.category in {'thing', 'rule'} and (
                '~activationFeature' in decl.body or '~activationFeature' in decl.defaults
            ) and decl.qualified not in self.support:
                raise ValueError(f'Unregistered activation support: {decl.qualified}')
        if set(self.support.values()) != self.features:
            raise ValueError('Every activation feature needs registered support')
        self.assets = {}
        asset_body = self.declarations['FeedbackAsset'].body
        members = list(re.finditer(r'^    (\w+)\s*\{([^{}]*)\}', asset_body, re.M))
        residue = asset_body
        for match in reversed(members):
            residue = residue[:match.start()] + residue[match.end():]
        if residue.strip(' \t\r\n,'):
            raise ValueError('Every resource member needs explicit literal modalities')
        for match in members:
            name = match[1]
            modalities = metadata(match[2], 'modalities', 'FeedbackModality [1..* unique]', 'FeedbackModality', True)
            if name in self.assets or not modalities or not modalities <= self.modalities:
                raise ValueError(f'{name}: missing, duplicate or unknown asset modalities')
            self.assets[name] = modalities
        if not self.assets:
            raise ValueError('Expected a closed resource family with explicit member metadata')
        self.tests = {d.qualified: d for d in self.declarations.values() if d.category == 'test'}
        self.checks = {}
        for key, decl in self.tests.items():
            if decl.path != 'scenarios':
                raise ValueError('This bounded planner supports tests only in path scenarios')
            concerns = effective(decl, 'checks', 'configuration.TestConcern [1..* unique]', 'configuration.TestConcern', True)
            if not concerns <= self.concerns:
                raise ValueError(f'{key}: unknown test concern')
            self.checks[key] = concerns
        if not self.tests:
            raise ValueError('No scenario declarations found')
        if set().union(*self.checks.values()) != self.concerns:
            raise ValueError('Every declared concern needs at least one scenario')
        for decl in self.declarations.values():
            if decl.category != 'test' and any(
                re.search(r'\b' + re.escape(test.name) + r'\b', decl.body)
                for test in self.tests.values()
            ):
                raise ValueError('Test references outside scenario bodies require a resolved compiler call graph')
        self.calls = {key: self.test_calls(decl) for key, decl in self.tests.items()}
        # Validate every world and call graph, even when selecting only some roots.
        for key in self.tests:
            self.closure(key)
            self.activation(self.tests[key])

    def reference(self, name: str) -> Declaration:
        decl = self.declarations.get(name.rsplit('.', 1)[-1])
        if decl is None or ('.' in name and name != decl.qualified):
            raise ValueError(f'Unknown catalogue reference: {name}')
        return decl

    def enum(self, name: str) -> frozenset[str]:
        decl = self.declarations[name]
        if decl.category != 'family' or not re.fullmatch(r'\s*\w+(?:\s*,\s*\w+)*\s*', decl.body):
            raise ValueError(f'{name}: unsupported enum definition')
        return frozenset(re.findall(r'\w+', decl.body))

    def test_calls(self, decl: Declaration) -> frozenset[str]:
        calls = set()
        if re.search(r'\bfrom\b', decl.body):
            raise ValueError('Foreign test bodies require a resolved compiler call graph')
        for test in self.tests.values():
            for match in re.finditer(r'(?<![\w.])(?:[a-z]\w*\.)*' + re.escape(test.name) + r'\b', decl.body):
                self.reference(match[0])
                if not re.match(r'\s*\(', decl.body[match.end():]):
                    raise ValueError('Indirect test references require a resolved compiler call graph')
                calls.add(test.qualified)
        return frozenset(calls)

    def closure(self, root: str) -> set[str]:
        seen, active = set(), set()
        def visit(key):
            if key in active:
                raise ValueError(f'Cyclic test calls: {key}')
            if key in seen:
                return
            active.add(key)
            for child in self.calls[key]:
                visit(child)
            active.remove(key)
            seen.add(key)
        visit(root)
        return seen

    def activation(self, test: Declaration) -> set[str]:
        matches = list(re.finditer(r'start with\s*\{([^{}]+)\}', test.body))
        if len(matches) != 1:
            raise ValueError(f'{test.qualified}: unsupported start template')
        match = matches[0]
        call = re.fullmatch(r'\s*ActivationSelection\((\[[^\]]*\])?\)\.declarations\s*,(.*)', match[1], re.S)
        if not call:
            raise ValueError(f'{test.qualified}: expected feature selection and explicit fixtures')
        requested = {'Core'}
        if call[1]:
            for token in call[1][1:-1].split(','):
                if not re.fullmatch(r'\s*ActivationFeature\.[A-Z]\w*\s*', token):
                    raise ValueError('Unsupported activation feature request')
                requested.add(token.strip().rsplit('.', 1)[1])
        if not requested <= self.features:
            raise ValueError('Unknown requested activation feature')
        result = {name for name, feature in self.support.items() if feature in requested}
        for name in call[2].split(','):
            decl = self.reference(name.strip())
            if decl.category not in {'thing', 'rule'}:
                raise ValueError(f'{name}: not an activatable fixture')
            result.add(decl.qualified)
        return result

    def plan(self, concerns: list[str]) -> dict:
        requested = set(concerns)
        if not requested <= self.concerns:
            raise ValueError('Unknown requested concern: ' + ', '.join(sorted(requested - self.concerns)))
        roots = sorted(key for key in self.tests if not requested or self.checks[key] & requested)
        if not roots:
            raise ValueError('No scenarios match the requested concerns')
        worlds = []
        for root in roots:
            closure = self.closure(root)
            activation = set().union(*(self.activation(self.tests[key]) for key in closure))
            worlds.append({'root': root, 'tests': sorted(closure), 'activation': sorted(activation)})
        return {'kind': 'bounded-source-plan', 'executesMud': False, 'worlds': worlds}


def main(argv=None) -> int:
    invocation = 'python tooling/examples/spell_metadata.py'
    catalogue = HelpCatalogue(product='MUD SPELL METADATA', version='',
        description='Validate the spell example metadata and print a source-only scenario plan.',
        invocation=invocation, groups=(), commands=(),
        usage=(f'{invocation} [--concern NAME ...] [--root PATH]',),
        global_items=(HelpItem('--concern NAME', 'Select a concern; repeat for union selection. Default: all scenarios.'),
                      HelpItem('--root PATH', 'Example directory. Default: notes/examples/duelo-spellcasting.'),
                      HelpItem('--colour auto|always|never', 'Control diagnostic colour. Default: auto; respects NO_COLOR.'),
                      HelpItem('--ascii', 'Use ASCII diagnostic symbols.')),
        notes=('Stdout is JSON. This does not compile or execute Mud, inspect Unity or simulate the runtime.',),
        show_help_on_empty=False)
    parser = MudArgumentParser(prog=invocation)
    parser.add_argument('--concern', action='append', default=[])
    parser.add_argument('--root', type=Path, default=EXAMPLE)
    add_presentation_arguments(parser)
    parsed = parse_cli(parser, catalogue, argv)
    if parsed.exit_code is not None:
        return parsed.exit_code
    try:
        result = Inventory(parsed.arguments.root).plan(parsed.arguments.concern)
    except (ValueError, KeyError, OSError) as exc:
        return failure(parsed.ui, 'Spell metadata validation failed.', code='Mud.Example.Metadata', details=str(exc))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
