'''
Look at every Wikipedia article under the `Units of Measurement` category,
and write them to a Markdown file as a to-do list.
'''
import wikipediaapi
ww = wikipediaapi.Wikipedia('Noether unit scanner (mia@yunru.se)', 'en')


def fetch_members(
    category: wikipediaapi.WikipediaPage,
    max_depth: int,
    exclude: set[str] = set(),
    exclude_duplicates: bool = False,
    *,
    _depth: int = 0
):
    for name, member in category.categorymembers.items():
        if member.title in exclude:
            continue
        if exclude_duplicates:
            exclude.add(member.title)
        yield _depth, member
        if name.startswith('Category:'):
            if _depth <= max_depth:
                yield from fetch_members(member, max_depth, exclude, exclude_duplicates, _depth=_depth+1)


cat = ww.page('Category:Units of measurement')
exclude = {
    'Years', 'Decades', 'Centuries',  # just lists of years
    'Category:Dimensional analysis',  # some 7,000 articles of nonunits

}

for d, page in fetch_members(cat, 5, exclude, True):
    print(f'{"  "*d}- [ ] [{page.title}]({page.fullurl})')
