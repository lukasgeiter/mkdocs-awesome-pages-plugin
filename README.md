# MkDocs Awesome Pages Plugin [![Build Status][travis-status]][travis-link]

*An MkDocs plugin that simplifies configuring page titles and their order*

The awesome-pages plugin allows you to customize how your pages show up the navigation of your MkDocs without having to configure the full structure in your `mkdocs.yml`. It extracts the title from your markdown files and gives you detailed control using a small configuration file directly placed in the relevant directory of your documentation.

> **Note:** This plugin works best without a `pages` entry in your `mkdocs.yml`. Having a `pages` entry is supported, but you might not get the results you expect, especially if your `pages` structure doesn't match the file structure.

<br/>

## Installation

> **Note:** This package requires MkDown version 0.17 or higher. 

Install the package with pip:

```yaml
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

### Extract Page Titles from Markdown

The plugin extracts the H1 title (only `#` syntax is supported) from every page and uses it for the title in the navigation.

### Set Directory Title

Create a YAML file named `.pages` in a directory and set the `title` to override the title of that directory in the navigation:

```yaml
title: Page Title
```

### Arrange Pages

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
        disable_auto_arrange_index: true
```

### `filename`

Name of the file used to configure pages of a directory. Default is `.pages`

### `disable_auto_arrange_index`

Disable the behavior of automatically putting the page with filename `index.*` at the beginning if there is no order specified in `arrange`. Default is `false`

<br/>

## Contributing

From reporting a bug to submitting a pull request: every contribution is appreciated and welcome.
Report bugs, ask questions and request features using [Github issues][github-issues].
If you want to contribute to the code of this project, please read the [Contribution Guidelines][contributing].

[travis-status]: https://travis-ci.org/lukasgeiter/mkdocs-awesome-pages-plugin.svg?branch=master
[travis-link]: https://travis-ci.org/lukasgeiter/mkdocs-awesome-pages-plugin
[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[github-issues]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/issues
[contributing]: CONTRIBUTING.md
