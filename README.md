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

## CI Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| [`build-on-pr.yml`](.github/workflows/build-on-pr.yml) | Pull request | Builds the RPMs so reviewers can verify the package still builds. Read-only — never publishes. |
| [`pkg-release.yml`](.github/workflows/pkg-release.yml) | Manual (`workflow_dispatch`) | Build and publish the RPM(s) to Artifactory, behind an approval gate. |

The GitHub Actions workflows use the shared
[`qcom-rpm-utils`](https://github.com/qualcomm-linux/qcom-rpm-utils) build
environment. They run `rpmbuild` inside the prebuilt `rpm-builder` container
image for the runner's host architecture.

---

## Repository layout

The `c10s` branch contains the RPM packaging files:

| File | Purpose |
|---|---|
| `gbm-msm-backend.spec` | Defines and builds the RPM package. |
| `gbm-msm-backend-fix-libdir.patch` | Replaces the upstream Debian-specific library-directory lookup and installs the format-alignment XML data. |
| `sources` | SHA-512 checksum for the upstream source archive. |
| `README.md` | Package and repository documentation. |
| `LICENSE.txt` | License for the RPM packaging repository. |

The source archive is not committed to this repository. The spec file's
`Source0` points to the upstream release, and the checksum in `sources` is
verified before the RPM is built.

---

## Packages

### `gbm-msm-backend`

The runtime package. It installs:

- `/usr/lib64/gbm/msm_gbm.so` — the Mesa GBM backend module.
- `/usr/lib64/gbm/default_fmt_alignment.xml` — format-alignment data used by the backend.

### `gbm-msm-backend-devel`

The development package. It installs:

- `/usr/include/gbm_msm.h` — the public header required by downstream software
  that includes `gbm_msm.h` while compiling.

---

## Installation

Install the package on the target device:

```bash
sudo dnf install gbm-msm-backend
```

```bash
sudo dnf install gbm-msm-backend-devel
```

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
4. Commit the spec + `sources`, open a PR (build verifies it), merge, then run
   **Release**. The first release fetches the new upstream tarball, verifies it,
   and caches it back to Artifactory automatically.

## License

This project is licensed under the BSD 3-Clause License. See [LICENSE.txt](LICENSE.txt) for the complete license text.
The upstream GBM MSM backend is licensed separately under
`BSD-3-Clause`, as declared in `gbm-msm-backend.spec`.
