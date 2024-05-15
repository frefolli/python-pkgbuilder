# Pkgbuilder

Declarative PKGBUILD automatic generation

# Usage

`python -m pkgbuilder` or `pkgbuilder-cli` will generate the PKGBUILD.

In order to include this script in your delivery process the version field must be taken into account. For now an option allows you to override version specification that would be loaded from `pkgbuild.yaml`. This is *NOT* the way to assert versioning in a github/gitlab/whatever workflow at all.
Take this repo as an example of a delivery macro for Github Actions: the action calls directly the pkgbuilder in this repo (but it could be fetched, and will be in future, in other ways such as using an Arch Container or wget-ing it). The version has already been modified inside `pkgbuild.yaml` because also `pyproject.toml` needs a version as well.
The master branch uses `${next-release}-beta` version for PKGBUILD and `${next-release}-beta` as version for hatchling. When and if the workflow would be executed on normal non-semver (check the regex in the [workflow file](.github/workflows/release.yml)) branches like `master`, a release tag `vmaster` will be created. This happens also for semver branches and this is why when releasing code you *SHOULD* fork `x.y.z` from `master`, and apply a commit in which you set versions.

Since I'm trying to resist the urge to build the definitive tool that could master all, this how you *SHOULD* update versions. Btw, other workarounds are possible too but I'm not recommending to spend 10 minutes to setup an automation for a 15s task.
If and only if there would be such tool, it will be in another project.

# Installation

## Arch Linux

Download PKGBUILD from Releases and `makepkg -si` it.

## Manual Packaging

Executing `make package` will build a package instead of a python wheel, therefore you should be able to install the pip package inside `dist/`.
