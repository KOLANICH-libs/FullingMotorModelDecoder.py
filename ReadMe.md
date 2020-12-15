FullingMotorModelDecoder.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===========================
[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/FullingMotorModelDecoder.py/workflows/CI/master/FullingMotorModelDecoder-0.CI-py3-none-any.whl)
~~[![GitHub Actions](https://github.com/KOLANICH-libs/FullingMotorModelDecoder.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/FullingMotorModelDecoder.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/FullingMotorModelDecoder.py.svg)](https://libraries.io/github/KOLANICH-libs/FullingMotorModelDecoder.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

This is a library to decode motor model numbers of Changzhou Fulling Motor Co., Ltd motors and gearboxes. The author and the library are NOT affiliated to the company.

Motors dataset [on csvbase<img src="https://csvbase.com/static/logo/192x192.png" height="12px" width="12px"/>](https://csvbase.com/KOLANICH/FullingMotors-motors).

!!!! **Currently doesn't fully work** !!!! - works only for motors, not gearboxes.

Docs on the format:
* [Delta Line Full Catalogue 2020-05](https://lotax.se/images/pdfs/Delta_Line_-_Fulling_Full_Catalogue_Edition_2020-05.pdf) (search `Codification`)
* [Catalogue 2018](https://www.europages.com/filestore/gallery/61/b7/15265927_7b1595da.pdf)  (search `Codification`)
* https://andrives.se/onewebmedia/emb%20FL%20stepper%20katalog.pdf

The docs seem to be not describing the actual format used and docs from different sourcess seem to contradict each other. Had to reverse engineer from samples.
