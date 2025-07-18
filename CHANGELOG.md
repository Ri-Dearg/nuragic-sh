# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v4.1.2] - 2025-07-18
### :bug: Bug Fixes
- [`2ea415b`](https://github.com/Ri-Dearg/nuragic-sh/commit/2ea415b977a276959513e8c8e2952809c0078e43) - **shop**: remove cache from i18n *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*

### :recycle: Refactors
- [`67f3a8a`](https://github.com/Ri-Dearg/nuragic-sh/commit/67f3a8a2f7ed9cf64944b9a0abff106c42b6cc40) - **db**: add bigautofield migration *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v4.1.1] - 2025-07-02
### :bug: Bug Fixes
- [`b4a8242`](https://github.com/Ri-Dearg/nuragic-sh/commit/b4a824235c0d2fc66d73f060b414d0c406742129) - **orders**: remove lang prefix webhook *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*

### :white_check_mark: Tests
- [`4961ce3`](https://github.com/Ri-Dearg/nuragic-sh/commit/4961ce33424e96176689f56dd1b91fac0574d85c) - **tests**: correct namespace for webhook *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v4.1.0] - 2025-06-19
### :sparkles: New Features
- [`9d28c53`](https://github.com/Ri-Dearg/nuragic-sh/commit/9d28c53d6b0d91982ed403f1058835f056a9e368) - **seo**: add robot view *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`084ad16`](https://github.com/Ri-Dearg/nuragic-sh/commit/084ad166a4cbfc4b254750212555198692249504) - **seo**: add robot.txt *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`92cd66d`](https://github.com/Ri-Dearg/nuragic-sh/commit/92cd66d456a759e96b06d3af0844fccc020b24d7) - **seo**: add sitemap class for static pages *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`97aa46e`](https://github.com/Ri-Dearg/nuragic-sh/commit/97aa46ecf553524fdae11798ddccc735288d7b76) - **seo**: add basic sitemap *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`f402008`](https://github.com/Ri-Dearg/nuragic-sh/commit/f40200833cac2c4dc21bc439198ce1ac8695c06c) - **seo**: add sitemap for info *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`1345c50`](https://github.com/Ri-Dearg/nuragic-sh/commit/1345c503325ec500d4fcdf189149db115c3867a5) - **seo**: create sitemap py *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`17f4bc9`](https://github.com/Ri-Dearg/nuragic-sh/commit/17f4bc91af7b136a6e79074952dd330c90962b8c) - **seo**: add policy sitemap view *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`8199537`](https://github.com/Ri-Dearg/nuragic-sh/commit/81995373396caf6d71d86b4f11fc5a264d184ae0) - **seo**: add shop sitemap *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`a7ba7f3`](https://github.com/Ri-Dearg/nuragic-sh/commit/a7ba7f30217668550678bf018f661f93cf12b15c) - **seo**: add allauth urls *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*

### :bug: Bug Fixes
- [`b6d57e1`](https://github.com/Ri-Dearg/nuragic-sh/commit/b6d57e15115ad4f95000854de95fcaaf3f738c05) - **seo**: add absolute url for sitemap *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`454fece`](https://github.com/Ri-Dearg/nuragic-sh/commit/454fecea6bbabad238b8ac1e13bf5e9656239186) - **tests**: fix newsletter test *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`674ef9d`](https://github.com/Ri-Dearg/nuragic-sh/commit/674ef9df89ce2a1fd08ed90996e3c100c9f7e445) - **shop**: fix products  context for new urls *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`1a7a614`](https://github.com/Ri-Dearg/nuragic-sh/commit/1a7a614b34375d9e049c34cddb555cfccbe66389) - **tests**: use reverse url for test *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`0103a2a`](https://github.com/Ri-Dearg/nuragic-sh/commit/0103a2ad2bfe28ca07016d3ba8fd0d8aceb860c0) - **tests**: use reverse for checkout tests *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*

### :recycle: Refactors
- [`53a926c`](https://github.com/Ri-Dearg/nuragic-sh/commit/53a926c5ed4237cd974f20068dfebb26a8572c6f) - **seo**: include more urls in il8n *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`8c3c24b`](https://github.com/Ri-Dearg/nuragic-sh/commit/8c3c24b5f25f0c38189ef3b131d264e8c70deb04) - **seo**: remove robots from sitemap *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`ff1aa2e`](https://github.com/Ri-Dearg/nuragic-sh/commit/ff1aa2eeaa818eebe72555f834315c111aab9695) - **tests**: reorder imports *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*

### :white_check_mark: Tests
- [`636a7ad`](https://github.com/Ri-Dearg/nuragic-sh/commit/636a7ad9c3167c00086165ed2dd3c805ab1a1a1a) - **tests**: fix adapter redirection *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`20c3fab`](https://github.com/Ri-Dearg/nuragic-sh/commit/20c3fabbf96db09173c8fab88cb6a94e9b34dc76) - **tests**: fix assertTrue test *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`d10135e`](https://github.com/Ri-Dearg/nuragic-sh/commit/d10135ed845d39c62c608665b3913f060096bb9b) - **tests**: update tests to use reverse *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*

### :wrench: Chores
- [`29105e3`](https://github.com/Ri-Dearg/nuragic-sh/commit/29105e3dce0b1334a511635cdadf7002b04d2ad5) - **req**: remove unused files *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v4.0.3] - 2025-06-19
### :bug: Bug Fixes
- [`d23430c`](https://github.com/Ri-Dearg/nuragic-sh/commit/d23430c712c0f25e6b408997cb2b3688c833d26b) - **tests**: update spoof file to include charge *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`3974e9f`](https://github.com/Ri-Dearg/nuragic-sh/commit/3974e9f9bdcac1230a8be32c8312abc8f8fa0383) - **orders**: webhook mpw uses latest_charge *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v4.0.2] - 2025-06-10
### :bug: Bug Fixes
- [`6338d25`](https://github.com/Ri-Dearg/nuragic-sh/commit/6338d25ff649c91d38a3745f3a8480752233e9d3) - **content**: fix spelling errors *(PR [#161](https://github.com/Ri-Dearg/nuragic-sh/pull/161) by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v4.0.1] - 2025-05-08
### :bug: Bug Fixes
- [`dccc952`](https://github.com/Ri-Dearg/nuragic-sh/commit/dccc95208f8d73031398d7069c55e67d4c5d9f67) - **content**: fix spelling errors *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v4.0.0] - 2025-05-06
### :boom: BREAKING CHANGES
- due to [`683ab64`](https://github.com/Ri-Dearg/nuragic-sh/commit/683ab642bd71d43cf4f71662dbc39fc4f9c48b80) - upgrade django to 5.2 *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*:

  upgrade django to 5.2


### :recycle: Refactors
- [`7cd87cd`](https://github.com/Ri-Dearg/nuragic-sh/commit/7cd87cd546c5841786793c6fe31ef001bf7fc52c) - **req**: remove depracted setting *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v3.0.3] - 2025-05-06
### :white_check_mark: Tests
- [`889a3e5`](https://github.com/Ri-Dearg/nuragic-sh/commit/889a3e5e8b198383084163f5e8294f7cbe0cbf15) - **orders**: add foundation for webhook testing. *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`7c9c418`](https://github.com/Ri-Dearg/nuragic-sh/commit/7c9c41837112eb8c0fda6cd0ff9390cd10e81702) - **orders**: test invalid data in webhook *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`8e86efa`](https://github.com/Ri-Dearg/nuragic-sh/commit/8e86efad86ff5e1240e7cf919a99aca943a40132) - **tests**: add payment_intent.succeeded json *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`7b1d53d`](https://github.com/Ri-Dearg/nuragic-sh/commit/7b1d53d480e5b8f2dbc44356fc21016f5d8744da) - **tests**: add test for payment success order *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`b67e3d3`](https://github.com/Ri-Dearg/nuragic-sh/commit/b67e3d3896fdb153ded314c680dcdce690a6e29e) - **tests**: add test for unhandled event *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*

### :wrench: Chores
- [`fbda908`](https://github.com/Ri-Dearg/nuragic-sh/commit/fbda9089aa4f69c8f90619ca4d04b88a56e9e7fa) - update gitignore to ignore test venv *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v3.0.2] - 2025-04-08
### :bug: Bug Fixes
- [`d009162`](https://github.com/Ri-Dearg/nuragic-sh/commit/d009162fb900e523d30636c53610b63cb288351f) - **orders**: updating total now runs save function *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`dfaa6cf`](https://github.com/Ri-Dearg/nuragic-sh/commit/dfaa6cfe83b69005979dfee430814e496e8266f0) - **orders**: pass delivery correctly to webhook *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*

### :recycle: Refactors
- [`da781ef`](https://github.com/Ri-Dearg/nuragic-sh/commit/da781ef4a4481e9096b17e0d1e08d420560bf90a) - remove unused code *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v3.0.1] - 2025-02-07
### :bug: Bug Fixes
- [`0e24356`](https://github.com/Ri-Dearg/nuragic-sh/commit/0e243565a7c1f6eeaa08a67212c019cb84695461) - update versioning to use branches correctly *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v3.0.0] - 2025-02-06
### :boom: BREAKING CHANGES
- due to [`58bfd0f`](https://github.com/Ri-Dearg/nuragic-sh/commit/58bfd0f519959fc1cdc0e06df611f0c347305f65) - upgrade psycopg to 3 *(PR [#127](https://github.com/Ri-Dearg/nuragic-sh/pull/127) by [@Ri-Dearg](https://github.com/Ri-Dearg))*:

  upgrade psycopg to 3 (#127)



## [v2.0.0] - 2025-02-06
### :boom: BREAKING CHANGES
- due to [`70884c7`](https://github.com/Ri-Dearg/nuragic-sh/commit/70884c72ce700e0706b890edd4ec27dcaf625dfb) - upgrade psycopg to 3 *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*:

  upgrade psycopg to 3



## [v1.0.2] - 2025-02-06
### :bug: Bug Fixes
- [`86195b3`](https://github.com/Ri-Dearg/nuragic-sh/commit/86195b3ef253dfcbff6e231378da58d340eedda1) - compare against own branch *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*


## [v1.0.1] - 2025-02-06
### :bug: Bug Fixes
- [`49f3d86`](https://github.com/Ri-Dearg/nuragic-sh/commit/49f3d866f889ebe2eae8047b30648d0efded4c22) - template typo and email server update. *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`24bd3cd`](https://github.com/Ri-Dearg/nuragic-sh/commit/24bd3cddf6ebec2ab631f0164792525e46942960) - billing postcode not saving *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`18468c0`](https://github.com/Ri-Dearg/nuragic-sh/commit/18468c02499b999873d3d9af9f4af2f535753f2c) - Order email creation *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`f1f8d3a`](https://github.com/Ri-Dearg/nuragic-sh/commit/f1f8d3aedf06321a638739888020d37879dcd91c) - Webhook now waits for order cheking thread *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*
- [`8301c5e`](https://github.com/Ri-Dearg/nuragic-sh/commit/8301c5e647f2b4c5058ad71f74a47b021a2a7f82) - intent description attr reference changed *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*

### :wrench: Chores
- [`fa70aff`](https://github.com/Ri-Dearg/nuragic-sh/commit/fa70aff16eac22f4286fcf37b978cdee9d9d8927) - add media folder to gitignore *(commit by [@Ri-Dearg](https://github.com/Ri-Dearg))*

[v1.0.1]: https://github.com/Ri-Dearg/nuragic-sh/compare/v1.0.0...v1.0.1
[v1.0.2]: https://github.com/Ri-Dearg/nuragic-sh/compare/v1.0.1...v1.0.2
[v2.0.0]: https://github.com/Ri-Dearg/nuragic-sh/compare/v1.0.2...v2.0.0
[v3.0.0]: https://github.com/Ri-Dearg/nuragic-sh/compare/v2.0.0...v3.0.0
[v3.0.1]: https://github.com/Ri-Dearg/nuragic-sh/compare/v3.0.0...v3.0.1
[v3.0.2]: https://github.com/Ri-Dearg/nuragic-sh/compare/v3.0.1...v3.0.2
[v3.0.3]: https://github.com/Ri-Dearg/nuragic-sh/compare/v3.0.2...v3.0.3
[v4.0.0]: https://github.com/Ri-Dearg/nuragic-sh/compare/v3.0.3...v4.0.0
[v4.0.1]: https://github.com/Ri-Dearg/nuragic-sh/compare/v4.0.0...v4.0.1
[v4.0.2]: https://github.com/Ri-Dearg/nuragic-sh/compare/v4.0.1...v4.0.2
[v4.0.3]: https://github.com/Ri-Dearg/nuragic-sh/compare/v4.0.2...v4.0.3
[v4.1.0]: https://github.com/Ri-Dearg/nuragic-sh/compare/v4.0.3...v4.1.0
[v4.1.1]: https://github.com/Ri-Dearg/nuragic-sh/compare/v4.1.0...v4.1.1
[v4.1.2]: https://github.com/Ri-Dearg/nuragic-sh/compare/v4.1.1...v4.1.2
