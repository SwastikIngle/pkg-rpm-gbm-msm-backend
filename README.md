<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# pkg-rpm-gbm-msm-backend

RPM packaging for the [Qualcomm Linux GBM MSM backend](https://github.com/qualcomm-linux/gbm-msm-backend)
on CentOS Stream 10 (aarch64).

`gbm-msm-backend` provides Mesa's GBM backend module for Qualcomm MSM/Adreno
platforms. The runtime package installs the `msm_gbm.so` GBM backend under
`/usr/lib64/gbm/`, together with its format-alignment XML data. The
`gbm-msm-backend-devel` package installs `gbm_msm.h` under `/usr/include/` for
software that needs to compile against the backend.

The package is maintained on the CentOS Stream 10 (`c10s`) branch and uses the
shared GitHub Actions build and release workflow.

> **Runtime note:** Mesa can load and probe this backend on a mainline MSM DRM
> system, but the current upstream backend requires the downstream KGSL sysfs
> path (`/sys/class/kgsl/kgsl-3d0/`) before it creates a device. Therefore, on a
> mainline DRM/MSM system without KGSL, Mesa falls back to its standard GBM path
> rather than activating this backend.

## CI Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| [`build-on-pr.yml`](.github/workflows/build-on-pr.yml) | Pull request (except Markdown-only changes) | Builds the RPMs so reviewers can verify the package still builds. Read-only — never publishes. |
| [`pkg-release.yml`](.github/workflows/pkg-release.yml) | Manual (`workflow_dispatch`) | Builds and publishes the RPMs to Artifactory after approval. |

The GitHub Actions workflows use the shared
[`qcom-rpm-utils`](https://github.com/qualcomm-linux/qcom-rpm-utils) build
environment. They run `rpmbuild` inside the prebuilt `rpm-builder` container
image for the runner's host architecture.

---

## Repository layout

The `c10s` branch contains the RPM packaging files:

| File | Purpose |
|---|---|
| `gbm-msm-backend.spec` | Defines the runtime and development RPM packages. |
| `gbm-msm-backend-fix-libdir.patch` | Replaces the upstream Debian-specific library-directory lookup and installs the format-alignment XML data. |
| `sources` | SHA-512 checksum for the upstream source archive. |
| `README.md` | Package and repository documentation. |
| `LICENSE.txt` | License for the RPM packaging repository. |

The source archive is not committed to this repository. `Source0` in the spec
points to the upstream release; the workflow obtains the archive from the
Artifactory lookaside cache when available, otherwise downloads it from
`Source0`, verifies the checksum in `sources`, and caches it during release.

---

## Packages

### `gbm-msm-backend`

The runtime package. It installs:

- `/usr/lib64/gbm/msm_gbm.so` — the Mesa GBM backend module.
- `/usr/lib64/gbm/default_fmt_alignment.xml` — format-alignment data used by the backend.

It requires `libdrm`, `mesa-libgbm`, `libxml2`, and `seatd`. `seatd` provides a
seat-management service for Weston and other DRM clients that need to open DRM
and input devices outside a logind-eligible desktop session, such as a serial
console session.

### `gbm-msm-backend-devel`

The development package. It installs:

- `/usr/include/gbm_msm.h` — the public header required by downstream software
  that includes `#include <gbm_msm.h>` while compiling against this backend.

The development package requires the exact matching architecture, version, and
release of `gbm-msm-backend`.

---

## Installation

Install the runtime backend from the configured CentOS Stream 10 repository:

```bash
sudo dnf install gbm-msm-backend
```

Install the header package when building software that includes `gbm_msm.h`:

```bash
sudo dnf install gbm-msm-backend-devel
```

The `-devel` package installs the matching runtime package automatically.

---

## Updating the package version

This is the standard workflow on `c10s`; source tarballs are not committed to
git:

1. Update `Version:` in `gbm-msm-backend.spec`. Update `Source0:` too if the
   upstream archive URL or naming convention has changed.
2. Download the matching upstream source archive using the filename expected by
   `Source0`, for example `gbm-msm-backend-<newversion>.tar.gz`.
3. Regenerate the source checksum:
   ```bash
   sha512sum --tag gbm-msm-backend-<newversion>.tar.gz > sources
   ```
4. Commit the spec and `sources` changes, then open a pull request targeting
   `c10s`. The PR workflow downloads the archive, verifies its checksum, and
   builds the RPMs.
5. After the PR is merged, run **Actions → Release → Run workflow** for `c10s`.
   An approved release publishes the RPMs to Artifactory and caches a newly
   fetched source archive for future builds.

## License

The RPM packaging files in this repository are licensed under the BSD 3-Clause
License. See [LICENSE.txt](LICENSE.txt) for the complete license text. The
upstream GBM MSM backend is licensed separately, as declared in
`gbm-msm-backend.spec`.
