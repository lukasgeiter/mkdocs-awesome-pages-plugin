# MkDocs Awesome Pages Plugin [![Build Status][travis-status]][travis-link]

*An MkDocs plugin that simplifies configuring page titles and their order*

The awesome-pages plugin allows you to customize how your pages show up the navigation of your MkDocs without having to configure the full structure in your `mkdocs.yml`. It gives you detailed control using a small configuration file directly placed in the relevant directory of your documentation.

> **Note:** This plugin works best without a `nav` or `pages` entry in your `mkdocs.yml`. Having a `nav` entry is supported, but you might not get the results you expect, especially if your `nav` structure doesn't match the file structure.

<br/>

## Installation

> **Note:** This package requires Python >=3.5 and MkDocs version 1.0 or higher.  
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

Create a YAML file named `.pages` in a directory and use the `nav` attribute to customize the navigation on that level. List the files and subdirectories in the order that they should appear in the navigation.

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

### Change Sort Order

Create a YAML file named `.pages` in a directory and set the `order` attribute to `asc` or `desc` to change the order of navigation items.

```yaml
order: desc
```

> **Note:** Unlike the default order, this does not distinguish between files and directories. Therefore pages and sections might get mixed.

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

If you only want to collapse certain pages, create a YAML file called `.pages` in the directory and set `collapse_single_pages` to `true`:

```yaml
collapse_single_pages: true
```

You may also enable collapsing globally using the plugin option and then use the `.pages` file to prevent certain sub-sections from being collapsed by setting `collapse_single_pages` to `false`.

> **Note:** This feature works recursively. That means it will also collapse multiple levels of single pages.

#### For a single page

If you want to enable or disable collapsing of a single page, without applying the setting recursively, create a YAML file called `.pages` in the directory and set `collapse` to `true` or `false`:

```yaml
collapse: true
```

### Hide Directory

Create a YAML file named `.pages` in a directory and set the `hide` attribute to `true` to hide the directory, including all sub-pages and sub-sections, from the navigation:

```yaml
hide: true
```

> **Note:** This option only hides the section from the navigation. It will still be included in the build and can be accessed under its URL.

### Set Directory Title

Create a YAML file named `.pages` in a directory and set the `title` to override the title of that directory in the navigation:

```yaml
title: Page Title
```

### Arrange Pages

> **Deprecated:** `arrange` will be removed in the next major release - [Use `nav` instead](#customize-navigation).

Create a YAML file named `.pages` in a directory and set the `arrange` attribute to change the order of how child pages appear in the navigation. This works for actual pages as well as subdirectories.

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

<br/>

## Options

You may customize the plugin by passing options in `mkdocs.yml`:

```yaml
plugins:
    - awesome-pages:
        filename: .index
        collapse_single_pages: true
        strict: false
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

<br/>

## Contributing

From reporting a bug to submitting a pull request: every contribution is appreciated and welcome.
Report bugs, ask questions and request features using [Github issues][github-issues].
If you want to contribute to the code of this project, please read the [Contribution Guidelines][contributing].

[travis-status]: https://travis-ci.org/lukasgeiter/mkdocs-awesome-pages-plugin.svg?branch=master
[travis-link]: https://travis-ci.org/lukasgeiter/mkdocs-awesome-pages-plugin
[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[github-v1]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/tree/v1
[github-issues]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/issues
[contributing]: CONTRIBUTING.md
