%global gbm_ver 1.2.6

Summary:        Mesa GBM backend for Qualcomm MSM/Adreno platforms
Name:           gbm-msm-backend
Version:        %{gbm_ver}
Release:        1%{?dist}
License:        BSD-3-Clause-Clear
URL:            https://github.com/qualcomm-linux/gbm-msm-backend
Source0:        https://github.com/qualcomm-linux/gbm-msm-backend/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Upstream meson.build shells out to Debian's dpkg-architecture to compute
# the install libdir, which doesn't exist on RPM-based distros. Use Meson's
# own prefix/libdir options instead.
# Temporary workaround for RPM packaging.
# Remove once upstream Meson files are updated.
Patch0:         gbm-msm-backend-fix-libdir.patch

BuildRequires:  gcc
BuildRequires:  meson >= 0.50
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libxml2-devel

Requires:       libdrm
Requires:       mesa-libgbm
Requires:       libxml2
# Weston (and other DRM/seat clients) need a seat manager to open
# /dev/dri/* and input devices when running outside a logind-eligible
# session (e.g. from a serial console) — logind alone isn't sufficient
# in that case. seatd provides that regardless of tty/session type.
Requires:       seatd

%description
Mesa GBM (Generic Buffer Manager) backend implementation for Qualcomm
MSM platforms. Provides hardware-accelerated buffer allocation for
Adreno GPUs via the GBM backend ABI.

%package devel
Summary:        Development header for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header file for building software against the Mesa GBM backend for
Qualcomm MSM/Adreno platforms.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%meson
%meson_build

%install
%meson_install
install -Dm644 src/gbm_msm.h %{buildroot}%{_includedir}/gbm_msm.h

%files
%license LICENSE
%{_libdir}/gbm/msm_gbm.so
%{_libdir}/gbm/default_fmt_alignment.xml

%files devel
%{_includedir}/gbm_msm.h

%changelog
* Thu Aug 20 2026 Qualcomm Linux <noreply@qualcomm.com> - 1.2.6-1
- Initial RPM packaging of gbm-msm-backend
