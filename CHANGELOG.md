# Changelog
All notable changes in pdfminer.six will be documented in this file. 

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Deprecated
- The argument `_py2_no_more_posargs` because Python2 is removed on January
, 2020 ([#328](https://github.com/pdfminer/pdfminer.six/pull/328) and 
[#307](https://github.com/pdfminer/pdfminer.six/pull/307))

### Added
- Support for extracting JBIG2 encoded images ([#311](https://github.com/pdfminer/pdfminer.six/pull/311) and [#46](https://github.com/pdfminer/pdfminer.six/pull/46))

### Fixed
- Unhandled AssertionError when dumping pdf containing reference to object id 0 ([#318](https://github.com/pdfminer/pdfminer.six/pull/318))

### Changed
- Using argparse instead of getopt for command line interface of dumppdf.py ([#321](https://github.com/pdfminer/pdfminer.six/pull/321))
- Refactor `LTLayoutContainer.group_textboxes` for a significant speed up in layout analysis ([#315](https://github.com/pdfminer/pdfminer.six/pull/315))

### Removed
- Files for external applications such as django, cgi and pyinstaller ([#314](https://github.com/pdfminer/pdfminer.six/issues/314))

## [20191020] - 2019-10-20

### Deprecated
- Support for Python 2 is dropped at January 1st, 2020 ([#307](https://github.com/pdfminer/pdfminer.six/pull/307))

### Added
- Contribution guidelines in [CONTRIBUTING.md](CONTRIBUTING.md) ([#259](https://github.com/pdfminer/pdfminer.six/pull/259))
- Support new encodings OneByteEncoding and DLIdent for CMaps ([#283](https://github.com/pdfminer/pdfminer.six/pull/283))

### Fixed
- Use `six.iteritems()` instead of `dict().iteritems()` to ensure Python2 and Python3 compatibility ([#274](https://github.com/pdfminer/pdfminer.six/pull/274))
- Properly convert Adobe Glyph names to unicode characters ([#263](https://github.com/pdfminer/pdfminer.six/pull/263))
- Allow CMap to be a content stream ([#283](https://github.com/pdfminer/pdfminer.six/pull/283))
- Resolve indirect objects for width and bounding boxes for fonts ([#273](https://github.com/pdfminer/pdfminer.six/pull/273))
- Actually updating stroke color in graphic state ([#298](https://github.com/pdfminer/pdfminer.six/pull/298))
- Interpret (invalid) negative font descent as a positive descent ([#203](https://github.com/pdfminer/pdfminer.six/pull/203))
- Correct colorspace comparision for images ([#132](https://github.com/pdfminer/pdfminer.six/pull/132))
- Allow for bounding boxes with zero height or width by removing assertion ([#246](https://github.com/pdfminer/pdfminer.six/pull/246))

### Changed
- All dependencies are managed in `setup.py` ([#306](https://github.com/pdfminer/pdfminer.six/pull/306) and [#219](https://github.com/pdfminer/pdfminer.six/pull/219))

## [20181108] - 2018-11-08

### Changed
- Speedup layout analysis ([#141](https://github.com/pdfminer/pdfminer.six/pull/141))
- Use argparse instead of replace deprecated getopt ([#173](https://github.com/pdfminer/pdfminer.six/pull/173))
- Allow pdfminer.six to be compiled with cython ([#142](https://github.com/pdfminer/pdfminer.six/pull/142))