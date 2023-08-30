# CHANGELOG - nginx

## Unreleased

## 6.0.0 / 2023-08-10

***Changed***:

* Bump the minimum base check version ([#15427](https://github.com/DataDog/integrations-core/pull/15427))

***Added***:

* Update generated config models ([#15212](https://github.com/DataDog/integrations-core/pull/15212))

***Fixed***:

* Fix types for generated config models ([#15334](https://github.com/DataDog/integrations-core/pull/15334))

## 5.4.2 / 2023-07-10

***Fixed***:

* Bump Python version from py3.8 to py3.9 ([#14701](https://github.com/DataDog/integrations-core/pull/14701))

## 5.4.1 / 2023-04-14 / Agent 7.45.0

***Fixed***:

* Fix a typo in the `disable_generic_tags` option description ([#14246](https://github.com/DataDog/integrations-core/pull/14246))

## 5.4.0 / 2022-09-16 / Agent 7.40.0

***Added***:

* Update HTTP config spec templates ([#12890](https://github.com/DataDog/integrations-core/pull/12890))

## 5.3.0 / 2022-04-05 / Agent 7.36.0

***Added***:

* Add metric_patterns options to filter all metric submission by a list of regexes ([#11695](https://github.com/DataDog/integrations-core/pull/11695))

***Fixed***:

* Remove outdated warning in the description for the `tls_ignore_warning` option ([#11591](https://github.com/DataDog/integrations-core/pull/11591))

## 5.2.1 / 2022-02-24 / Agent 7.35.0

***Fixed***:

* Adjust endpoint detection logic for warn log ([#11567](https://github.com/DataDog/integrations-core/pull/11567))

## 5.2.0 / 2022-02-19

***Added***:

* Add `pyproject.toml` file ([#11404](https://github.com/DataDog/integrations-core/pull/11404))

***Fixed***:

* Fix namespace packaging on Python 2 ([#11532](https://github.com/DataDog/integrations-core/pull/11532))

## 5.1.0 / 2022-02-03

***Added***:

* Allow for percentile aggregations for NGINX integration response time metrics ([#11252](https://github.com/DataDog/integrations-core/pull/11252))

***Fixed***:

* Instruct the user to fix the error ([#11107](https://github.com/DataDog/integrations-core/pull/11107))

## 5.0.0 / 2022-01-08 / Agent 7.34.0

***Changed***:

* Add `server` default group for all monitor special cases ([#10976](https://github.com/DataDog/integrations-core/pull/10976))

***Added***:

* Add option to dynamically determine what APIs to query for metrics ([#10815](https://github.com/DataDog/integrations-core/pull/10815))

***Fixed***:

* Bump base package ([#11061](https://github.com/DataDog/integrations-core/pull/11061))
* Add comment to autogenerated model files ([#10945](https://github.com/DataDog/integrations-core/pull/10945))
* Bump base package dependency ([#10930](https://github.com/DataDog/integrations-core/pull/10930))

## 4.1.0 / 2021-12-08

***Added***:

* Add support for NGINX Plus versions 4-7 ([#10750](https://github.com/DataDog/integrations-core/pull/10750))

## 4.0.0 / 2021-10-04 / Agent 7.32.0

***Changed***:

* Add disable generic tags option ([#10249](https://github.com/DataDog/integrations-core/pull/10249))

***Added***:

* Add HTTP option to control the size of streaming responses ([#10183](https://github.com/DataDog/integrations-core/pull/10183))
* Add allow_redirect option ([#10160](https://github.com/DataDog/integrations-core/pull/10160))
* Disable generic tags ([#10027](https://github.com/DataDog/integrations-core/pull/10027))

***Fixed***:

* Bump base package dependency ([#10218](https://github.com/DataDog/integrations-core/pull/10218))
* Fix the description of the `allow_redirects` HTTP option ([#10195](https://github.com/DataDog/integrations-core/pull/10195))

## 3.13.0 / 2021-08-22 / Agent 7.31.0

***Added***:

* Use `display_default` as a fallback for `default` when validating config models ([#9739](https://github.com/DataDog/integrations-core/pull/9739))

## 3.12.0 / 2021-04-19 / Agent 7.28.0

***Added***:

* Add runtime configuration validation ([#8962](https://github.com/DataDog/integrations-core/pull/8962))

## 3.11.2 / 2021-03-07 / Agent 7.27.0

***Fixed***:

* Rename config spec example consumer option `default` to `display_default` ([#8593](https://github.com/DataDog/integrations-core/pull/8593))
* Bump minimum base package version ([#8443](https://github.com/DataDog/integrations-core/pull/8443))

## 3.11.1 / 2021-01-26 / Agent 7.26.0

***Fixed***:

* Lower log level for version metadata submission ([#8448](https://github.com/DataDog/integrations-core/pull/8448))

## 3.11.0 / 2021-01-25

***Added***:

* Add support for nginx API v3 ([#8392](https://github.com/DataDog/integrations-core/pull/8392))

## 3.10.1 / 2020-11-16 / Agent 7.25.0

***Fixed***:

* Fix version metadata collection ([#7972](https://github.com/DataDog/integrations-core/pull/7972))

## 3.10.0 / 2020-10-31 / Agent 7.24.0

***Added***:

* Add ability to dynamically get authentication information ([#7660](https://github.com/DataDog/integrations-core/pull/7660))
* [doc] Add encoding in log config sample ([#7708](https://github.com/DataDog/integrations-core/pull/7708))

## 3.9.0 / 2020-09-21 / Agent 7.23.0

***Added***:

* Add RequestsWrapper option to support UTF-8 for basic auth ([#7441](https://github.com/DataDog/integrations-core/pull/7441))
* Option to disable stream api checking in Nginx Plus ([#7241](https://github.com/DataDog/integrations-core/pull/7241)) Thanks [szibis](https://github.com/szibis).

***Fixed***:

* Update proxy section in conf.yaml ([#7336](https://github.com/DataDog/integrations-core/pull/7336))

## 3.8.1 / 2020-08-10 / Agent 7.22.0

***Fixed***:

* Update logs config service field to optional ([#7209](https://github.com/DataDog/integrations-core/pull/7209))
* DOCS-838 Template wording ([#7038](https://github.com/DataDog/integrations-core/pull/7038))
* Update ntlm_domain example ([#7118](https://github.com/DataDog/integrations-core/pull/7118))

## 3.8.0 / 2020-06-29 / Agent 7.21.0

***Added***:

* Add note about warning concurrency ([#6967](https://github.com/DataDog/integrations-core/pull/6967))
* Add config specs ([#6797](https://github.com/DataDog/integrations-core/pull/6797))

***Fixed***:

* Fix template specs typos ([#6912](https://github.com/DataDog/integrations-core/pull/6912))

## 3.7.0 / 2020-05-17 / Agent 7.20.0

***Added***:

* Allow optional dependency installation for all checks ([#6589](https://github.com/DataDog/integrations-core/pull/6589))

## 3.6.1 / 2020-04-04 / Agent 7.19.0

***Fixed***:

* Remove logs sourcecategory ([#6121](https://github.com/DataDog/integrations-core/pull/6121))

## 3.6.0 / 2020-01-13 / Agent 7.17.0

***Added***:

* Use lazy logging format ([#5398](https://github.com/DataDog/integrations-core/pull/5398))
* Use lazy logging format ([#5377](https://github.com/DataDog/integrations-core/pull/5377))

***Fixed***:

* Handle missing version ([#5250](https://github.com/DataDog/integrations-core/pull/5250))

## 3.5.0 / 2019-12-02 / Agent 7.16.0

***Added***:

* Submit version metadata ([#4736](https://github.com/DataDog/integrations-core/pull/4736))

## 3.4.0 / 2019-10-11 / Agent 6.15.0

***Added***:

* Add option to override KRB5CCNAME env var ([#4578](https://github.com/DataDog/integrations-core/pull/4578))

## 3.3.0 / 2019-08-24 / Agent 6.14.0

***Added***:

* Add requests wrapper to Nginx ([#4268](https://github.com/DataDog/integrations-core/pull/4268))

## 3.2.0 / 2019-05-14 / Agent 6.12.0

***Added***:

* Simplify JSON flattening for timestamps and bool ([#3648](https://github.com/DataDog/integrations-core/pull/3648)) Thanks [jd](https://github.com/jd).
* Adhere to code style ([#3545](https://github.com/DataDog/integrations-core/pull/3545))

## 3.1.0 / 2019-01-04 / Agent 6.9.0

***Added***:

* Support Python 3 ([#2716](https://github.com/DataDog/integrations-core/pull/2716))

## 3.0.0 / 2018-09-04 / Agent 6.5.0

***Changed***:

* Send correct count values for NGINX ever increasing counters ([#2041](https://github.com/DataDog/integrations-core/pull/2041))

***Fixed***:

* Add data files to the wheel package ([#1727](https://github.com/DataDog/integrations-core/pull/1727))

## 2.2.0 / 2018-06-04

***Changed***:

* Log warning, not exception, when trying to collect stream metrics ([#1536](https://github.com/DataDog/integrations-core/pull/1536))

***Added***:

* Add support for VTS module ([#1295](https://github.com/DataDog/integrations-core/pull/1295)) Thanks [mattjbray](https://github.com/mattjbray)

## 2.1.0 / 2018-05-11

***Added***:

* Add custom tag support to service checks.

## 2.0.0 / 2018-03-23

***Added***:

* Better process status output for good metric names. Breaking if using the badly named metrics in app ([#1053](https://github)com/DataDog/integrations-core/issues/1053)

## 1.2.0 / 2018-02-13

***Added***:

* Make the check compatible with the new Plus API. [#1013](https://github.com/DataDog/integrations-core/issues/1013)
* Adding configuration for log collection in `conf.yaml`
* allows the bypassing of proxy settings ([#1051](https://github.com/DataDog/integrations-core/pull/1051))

## 1.1.0 / 2017-07-18

***Fixed***:

* adds duplicate nginx.upstream.peers.response.*xx_count metrics with type count. [#559](https://github.com/DataDog/integrations-core/issues/559)

## 1.0.0 / 2017-03-22

***Added***:

* adds nginx integration.