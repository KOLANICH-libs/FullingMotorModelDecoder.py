FullingMotorModelDecoder.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===========================
[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/FullingMotorModelDecoder.py/workflows/CI/master/FullingMotorModelDecoder-0.CI-py3-none-any.whl)
~~[![GitHub Actions](https://github.com/KOLANICH-libs/FullingMotorModelDecoder.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/FullingMotorModelDecoder.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/FullingMotorModelDecoder.py.svg)](https://libraries.io/github/KOLANICH-libs/FullingMotorModelDecoder.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

**We have moved to https://codeberg.org/KFmts/FullingMotorModelDecoder.py (the namespace has changed to `KFmts`, which groups packages related to parsing or serialization), grab new versions there.**

Under the disguise of "better security" Micro$oft-owned GitHub has [discriminated users of 1FA passwords](https://github.blog/2023-03-09-raising-the-bar-for-software-security-github-2fa-begins-march-13/) while having commercial interest in success and wide adoption of [FIDO 1FA specifications](https://fidoalliance.org/specifications/download/) and [Windows Hello implementation](https://support.microsoft.com/en-us/windows/passkeys-in-windows-301c8944-5ea2-452b-9886-97e4d2ef4422) which [it promotes as a replacement for passwords](https://github.blog/2023-07-12-introducing-passwordless-authentication-on-github-com/). It will result in dire consequencies and is competely inacceptable, [read why](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

If you don't want to participate in harming yourself, it is recommended to follow the lead and migrate somewhere away of GitHub and Micro$oft. Here is [the list of alternatives and rationales to do it](https://github.com/orgs/community/discussions/49869). If they delete the discussion, there are certain well-known places where you can get a copy of it. [Read why you should also leave GitHub](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

---

This is a library to decode motor model numbers of Changzhou Fulling Motor Co., Ltd motors and gearboxes. The author and the library are NOT affiliated to the company.

Motors dataset [on csvbase<img src="https://csvbase.com/static/logo/192x192.png" height="12px" width="12px"/>](https://csvbase.com/KOLANICH/FullingMotors-motors).

!!!! **Currently doesn't fully work** !!!! - works only for motors, not gearboxes.

Docs on the format:
* [Delta Line Full Catalogue 2020-05](https://lotax.se/images/pdfs/Delta_Line_-_Fulling_Full_Catalogue_Edition_2020-05.pdf) (search `Codification`)
* [Catalogue 2018](https://www.europages.com/filestore/gallery/61/b7/15265927_7b1595da.pdf)  (search `Codification`)
* https://andrives.se/onewebmedia/emb%20FL%20stepper%20katalog.pdf

The docs seem to be not describing the actual format used and docs from different sourcess seem to contradict each other. Had to reverse engineer from samples.
