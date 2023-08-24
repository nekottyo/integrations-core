# CHANGELOG - Nfsstat

## Unreleased

## 1.12.1 / 2023-08-18

***Fixed***:

* Update datadog-checks-base dependency version to 32.6.0 ([#15604](https://github.com/DataDog/integrations-core/pull/15604))

## 1.12.0 / 2023-08-10

***Added***:

* Update generated config models ([#15212](https://github.com/DataDog/integrations-core/pull/15212))

***Fixed***:

* Fix types for generated config models ([#15334](https://github.com/DataDog/integrations-core/pull/15334))

## 1.11.1 / 2023-07-10

***Fixed***:

* Bump Python version from py3.8 to py3.9 ([#14701](https://github.com/DataDog/integrations-core/pull/14701))

## 1.11.0 / 2022-04-05 / Agent 7.36.0

***Added***:

* Add metric_patterns options to filter all metric submission by a list of regexes ([#11695](https://github.com/DataDog/integrations-core/pull/11695))

## 1.10.0 / 2022-02-19 / Agent 7.35.0

***Added***:

* Add `pyproject.toml` file ([#11403](https://github.com/DataDog/integrations-core/pull/11403))

***Fixed***:

* Fix namespace packaging on Python 2 ([#11532](https://github.com/DataDog/integrations-core/pull/11532))

## 1.9.1 / 2022-01-08 / Agent 7.34.0

***Fixed***:

* Add comment to autogenerated model files ([#10945](https://github.com/DataDog/integrations-core/pull/10945))

## 1.9.0 / 2021-10-04 / Agent 7.32.0

***Added***:

* Disable generic tags ([#10027](https://github.com/DataDog/integrations-core/pull/10027))

## 1.8.0 / 2021-08-22 / Agent 7.31.0

***Added***:

* Use `display_default` as a fallback for `default` when validating config models ([#9739](https://github.com/DataDog/integrations-core/pull/9739))

## 1.7.0 / 2021-05-28 / Agent 7.29.0

***Added***:

* Add runtime configuration validation ([#8961](https://github.com/DataDog/integrations-core/pull/8961))

## 1.6.2 / 2021-03-07 / Agent 7.27.0

***Fixed***:

* Rename config spec example consumer option `default` to `display_default` ([#8593](https://github.com/DataDog/integrations-core/pull/8593))
* Bump minimum base package version ([#8443](https://github.com/DataDog/integrations-core/pull/8443))

## 1.6.1 / 2020-09-21 / Agent 7.23.0

***Fixed***:

* Fix style for the latest release of Black ([#7438](https://github.com/DataDog/integrations-core/pull/7438))

## 1.6.0 / 2020-06-29 / Agent 7.21.0

***Added***:

* Avoid logging warnings if AutoFS is enabled ([#6903](https://github.com/DataDog/integrations-core/pull/6903))
* Add specs and use new signature ([#6780](https://github.com/DataDog/integrations-core/pull/6780))

## 1.5.0 / 2020-05-17 / Agent 7.20.0

***Added***:

* Allow optional dependency installation for all checks ([#6589](https://github.com/DataDog/integrations-core/pull/6589))

***Fixed***:

* Fix nfsiostat command ([#6650](https://github.com/DataDog/integrations-core/pull/6650))

## 1.4.2 / 2020-04-04 / Agent 7.19.0

***Fixed***:

* Update deprecated imports ([#6088](https://github.com/DataDog/integrations-core/pull/6088))

## 1.4.1 / 2019-05-30 / Agent 6.12.0

***Fixed***:

* Fix non-ascii mounted folder name ([#3805](https://github.com/DataDog/integrations-core/pull/3805))

## 1.4.0 / 2019-05-14

***Added***:

* Adhere to code style ([#3544](https://github.com/DataDog/integrations-core/pull/3544))

## 1.3.0 / 2019-03-29 / Agent 6.11.0

***Added***:

* Support Python 3 ([#3228](https://github.com/DataDog/integrations-core/pull/3228))

## 1.2.0 / 2019-02-18 / Agent 6.10.0

***Added***:

* Don't raise Exception when No NFS mounts could be found ([#3069](https://github.com/DataDog/integrations-core/pull/3069))

## 1.1.0 / 2019-01-04 / Agent 6.9.0

***Added***:

* Support Python 3 ([#2775](https://github.com/DataDog/integrations-core/pull/2775))

## 1.0.0 / 2018-10-13 / Agent 6.6.0

***Added***:

* NFSIOStat Check ([#720](https://github.com/DataDog/integrations-core/pull/720))

## 0.2.1 / 2018-09-04 / Agent 6.5.0

***Fixed***:

* Add data files to the wheel package ([#1727](https://github.com/DataDog/integrations-core/pull/1727))

## 0.2.0 / 2018-03-23

***Added***:

* add custom tag support.

## 0.1.1 / 2018-02-13

***Fixed***:

* makes reports output stats in actual realtime ([#974](https://github.com/DataDog/integrations-core/pull/974))

## 0.1.0 / 2017-10-10

***Added***:

* adds nfsstat integration ([#720](https://github.com/DataDog/integrations-core/issues/720))