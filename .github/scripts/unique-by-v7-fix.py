from pathlib import Path


def replace(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one residue, found {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')


replace(
    'specification/07-concrete-grammar.md',
    'Without `ordered`, every ordinary branch is evaluated and all results are obtained; `unique` removes duplicate results:',
    'Without `ordered`, every ordinary branch is evaluated and all results are obtained; the effective uniqueness modifier then normalises them: ordinary `unique` removes repeated whole values and `unique by path` removes later equal-key results:'
)
replace(
    'specification/07-concrete-grammar.md',
    '`^=` accepts only `unique` collections.',
    '`^=` accepts only collections that guarantee whole-value uniqueness; ordinary `unique` and `unique by path` both satisfy that precondition.'
)
replace(
    'notes/decisions/ADR-080-higher-order-collection-algebra-and-updates.md',
    '- XOR retains the laws a reader expects because it operates only on `unique` sets.',
    '- XOR retains the laws a reader expects because it operates only on collections that guarantee whole-value uniqueness.'
)

plan = Path('.mud-patch-unique-by-plan.md')
plan.write_text(
    plan.read_text(encoding='utf-8')
    + '\n\n## Findings from the second full review\n\n'
      '- Replaced the stale `AllMatches` summary that mentioned only ordinary `unique`.\n'
      '- Generalised the remaining `^=` and XOR summaries from the `unique` spelling to the whole-value-uniqueness precondition supplied by either uniqueness mode.\n',
    encoding='utf-8',
)
