# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
