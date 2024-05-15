# Changelog

## 1.0.1

- Pkgbuilder wasn't considering runtime dependencies while forging the PKGBUILD file
- Using the new Action for pkgbuilder to call for instead of having to ship and maintain multiple copies of `pkgbuilder` around the world
- Upstream master ships `${next-release}-beta` too instead of `master`
- Now pkgbuilder writes a PKGBUILD file which path and name can be changed with `-o` option
