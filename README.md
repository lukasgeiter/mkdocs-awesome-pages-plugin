# MkDocs Awesome Pages Plugin [![Tests Status][status-tests-badge]][status-tests-link]

*An MkDocs plugin that simplifies configuring page titles and their order*

The awesome-pages plugin allows you to customize how your pages show up the navigation of your MkDocs without having to configure the full structure in your `mkdocs.yml`. It gives you detailed control using a small configuration file directly placed in the relevant directory of your documentation.

> **Note:** This plugin won't do anything if your `mkdocs.yml` defines a `nav` or `pages` entry. To make use of the features listed below, you'll either have to remove the entry completely or [add a `...` entry to it](#combine-custom-navigation--file-structure).

<br/>

## Installation

> **Note:** This package requires Python >=3.8.1 and MkDocs version 1.0 or higher.  
> If you're still on MkDocs 0.17 use [version 1 of this plugin][github-v1].

Install the package with pip:

```bash
pip install mkdocs-awesome-pages-plugin
```

Enable the plugin in your `mkdocs.yml`:

```yaml
plugins:
    - search
    - awesome-pages
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins]

<br/>

## Features

### Customize Navigation

Create a file named `.pages` in a directory and use the `nav` attribute to customize the navigation on that level. List the files and subdirectories in the order that they should appear in the navigation.

```yaml
nav:
    - subdirectory
    - page1.md
    - page2.md
```

#### Rest

Pages or sections that are not mentioned in the list will not appear in the navigation. However, you may include a `...`  entry to specify where all remaining items should be inserted.

```yaml
nav:
    - introduction.md
    - ...
    - summary.md
```

Furthermore, it is possible to filter the remaining items using glob patterns or regular expressions. For example to match only the Markdown files starting with `introduction-`.

```yaml
nav:
    - ... | introduction-*.md
    - ...
    - summary.md
```

> **Note:** The pattern is checked against the basename (folder- / filename) of remaining items - not their whole path.

For more details refer to the [Rest Filter Patterns](#rest-filter-patterns) section below.

#### Titles

You can optionally specify a title for the navigation entry.

```yaml
nav:
    - ...
    - First page: page1.md
```

> **Note:** Specifying a title for a directory containing a `.pages` file that defines a `title` has no effect.

#### Links

You can also use the `nav` attribute to add additional links to the navigation.

```yaml
nav:
    - ...
    - Link Title: https://lukasgeiter.com
```

#### Sections

You can group items by creating new sections.

```yaml
nav:
    - introduction.md
    - Section 1:
        - page1.md
        - page2.md
    - Section 2:
        - ...
```

### Change Sort Order

Create a file named `.pages` in a directory and set the `order` attribute to `asc` or `desc` to change the order of navigation items.

```yaml
order: desc
```

> **Note:** Unlike the default order, this does not distinguish between files and directories. Therefore pages and sections might get mixed.

### Natural Sort Type

Create a file named `.pages` in a directory and set the `sort_type` attribute to `natural` to use [natural sort order](https://en.wikipedia.org/wiki/Natural_sort_order).

This can be combined with `order` above.

```yaml
sort_type: natural
```

### Order Navigation By Preference

Create a file named `.pages` in a directory and set the `order_by` attribute to `filename` or `title` to change the order of navigation items.

```yaml
order_by: title
```

This can be combined with `order` and/or `sort_type` above. If `order` is not set it will order ascending. If no preference is set, it will order by filename.

### Collapse Single Nested Pages

> **Note:** This feature is disabled by default. More on how to use it below

If you have directories that only contain a single page, awesome-pages can "collapse" them, so the folder doesn't show up in the navigation.

For example if you have the following file structure:

```yaml
docs/
├─ section1/
│  ├─ img/
│  │  ├─ image1.png
│  │  └─ image2.png
│  └─ index.md # Section 1
└─ section2/
   └─ index.md # Section 2
```

The pages will appear in your navigation at the root level:

- Section 1
- Section 2

Instead of how MkDocs would display them by default:

- Section 1
  - Index
- Section 2
  - Index

#### For all pages

Collapsing can be enabled globally using the [`collapse_single_pages` option](#collapse_single_pages) in `mkdocs.yml`

#### For a sub-section

If you only want to collapse certain pages, create a file called `.pages` in the directory and set `collapse_single_pages` to `true`:

```yaml
collapse_single_pages: true
```

You may also enable collapsing globally using the plugin option and then use the `.pages` file to prevent certain sub-sections from being collapsed by setting `collapse_single_pages` to `false`.

> **Note:** This feature works recursively. That means it will also collapse multiple levels of single pages.

#### For a single page

If you want to enable or disable collapsing of a single page, without applying the setting recursively, create a file called `.pages` in the directory and set `collapse` to `true` or `false`:

```yaml
collapse: true
```

If you want to force the section to collapse even when having multiple children, add the flag `force_collapse`:

```yaml
collapse: true
force_collapse: true
```

Note that setting `collapse: false` will ignore `force_collapse`

### Hide Directory

Create a file named `.pages` in a directory and set the `hide` attribute to `true` to hide the directory, including all sub-pages and sub-sections, from the navigation:

```yaml
hide: true
```

> **Note:** This option only hides the section from the navigation. It will still be included in the build and can be accessed under its URL.

### Set Directory Title

Create a file named `.pages` in a directory and set the `title` to override the title of that directory in the navigation:

```yaml
title: Page Title
```

### Arrange Pages

> **Deprecated:** `arrange` will be removed in the next major release - [Use `nav` instead](#customize-navigation).

Create a file named `.pages` in a directory and set the `arrange` attribute to change the order of how child pages appear in the navigation. This works for actual pages as well as subdirectories.

```yaml
title: Page Title
arrange:
    - page1.md
    - page2.md
    - subdirectory
```

If you only specify *some* pages, they will be positioned at the beginning, followed by the other pages in their original order.

You may also include a `...` entry at some position to specify where the rest of the pages should be inserted:

```yaml
arrange:
    - introduction.md
    - ...
    - summary.md
```

In this example `introduction.md` is positioned at the beginning, `summary.md` at the end, and any other pages in between.

### Combine Custom Navigation & File Structure

MkDocs gives you two ways to define the structure of your navigation. Either create a custom navigation manually in `mkdocs.yml` or use the file structure to generate the navigation. This feature makes it possible to combine both methods. Allowing you to manually define parts of your navigation without having to list all files.

> **Note:** You can freely combine this with all the other features of this plugin. However they will only affect the part of the navigation that is not defined manually.

Use the `nav` entry in `mkdocs.yml` to define the custom part of your navigation. Include a `...` entry where you want the navigation tree of all remaining pages to be inserted.

The following examples are based on this file structure:

```yaml
docs/
├─ introduction.md
├─ page1.md
├─ page2.md
└─ folder/
   ├─ introduction.md
   ├─ page3.md
   └─ page4.md
```

If you wanted `introduction.md`, `page1.md` and `page2.md` to appear under their own section you could do this:

```yaml
nav:
    - Start:
        - introduction.md
        - page1.md
        - page2.md
    - ...
```

Which would result in the following navigation:

- Start
  - Introduction
  - Page 1
  - Page 2
- Folder
  - Introduction
  - Page 3
  - Page 4

The `...` entry can also be placed at a deeper level:

```yaml
nav:
    - page1.md
    - Rest:
        - ...
```

Which would result in the following navigation:

- Page 1
- Rest
  - Introduction
  - Page 2
  - Folder
    - Introduction
    - Page 3
    - Page 4

Furthermore, it is possible to filter the remaining items using glob patterns or regular expressions. For example to match only files named `introduction.md`.

```yaml
nav:
    - Introductions:
        - ... | **/introduction.md
    - ...
```

With the following result:

- Introductions
    - Introduction
    - Introduction
- Page 1
- Page 2
- Folder
    - Page 3
    - Page 4
    

> **Note:** The pattern is checked against the path relative to the docs directory.

For more details refer to the [Rest Filter Patterns](#rest-filter-patterns) section below.

By default, remaining items keep their hierarchical structure. You may add `flat` to flatten all the matching pages:

```yaml
nav:
    - page1.md
    - Rest:
        - ... | flat | **/introduction.md
        - ... | flat
```

- Page 1
- Rest
    - Introduction
    - Introduction
    - Page 2
    - Page 3
    - Page 4

<br/>

## Rest Filter Patterns

In all places where the rest entry (`...`) is allowed, you can also include a glob pattern or regular expression to filter the items to be displayed.

```yaml
nav:
    - ... | page-*.md
    - ... | regex=page-[0-9]+.md
```

The filter only operates on remaining items. This means it will not include items that are explicitly listed in the navigation or items that are matched by another filter that appears earlier in the configuration.

You may also include a rest entry without filter to act as a catch-all, inserting everything that is not matched by a filter.

### Syntax Details

Unless the filter starts with `regex=` it is interpreted as glob pattern, however you may also explicitly say so using `glob=`. The spaces around `...` are optional but recommended for readability.

> **Note:** Depending on the characters in your filter, you might also need to use quotes around the whole entry.

```yaml
nav:
    # equivalent glob entries
    - ... | page-*.md
    - ... | glob=page-*.md
    - ...|page-*.md
    - '... | page-*.md'

    # equivalent regex entries
    - ... | regex=page-[0-9]+.md
    - ...|regex=page-[0-9]+.md
    - '... | regex=page-[0-9]+.md'
```

<br/>

## Options

You may customize the plugin by passing options in `mkdocs.yml`:

```yaml
plugins:
    - awesome-pages:
        filename: .index
        collapse_single_pages: true
        strict: false
        order: asc
        sort_type: natural
        order_by: title
```

### `filename`

Name of the file used to configure pages of a directory. Default is `.pages`

### `collapse_single_pages`

Enable the collapsing of single nested pages. Default is `false`

### `strict`

Raise errors instead of warnings when:

- `arrange` entries cannot be found
- `nav` entries cannot be found

Default is `true`

### `order`, `sort_type` and `order_by`

Global fallback values for the Meta attributes. Default is `None` or `filename`.

<br/>

## Contributing

From reporting a bug to submitting a pull request: every contribution is appreciated and welcome.
Report bugs, ask questions and request features using [Github issues][github-issues].
If you want to contribute to the code of this project, please read the [Contribution Guidelines][contributing].

[status-tests-badge]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/actions/workflows/tests.yml/badge.svg
[status-tests-link]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/actions/workflows/tests.yml
[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[github-v1]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/tree/v1
[github-issues]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/issues
[contributing]: CONTRIBUTING.md
