#
# FUSE 3.2 specfile for CentOS 7.5 (and probably more)
# Originally from https://github.com/vmware/photon/
# Build with --nocheck to bypass tests
#
%if 0%{?rhel}
%{!?python3_pkgversion: %global python3_pkgversion 34}
%else
%{!?python3_pkgversion: %global python3_pkgversion 3}
%endif
%global python3_pkgprefix python%{python3_pkgversion}

# Undefined in openSUSE
%{!?__python3: %global __python3 python3}

Summary:        File System in Userspace (FUSE) utilities
Name:           fuse
Version:        3.2.6
Release:        2%{?dist}
License:        GPL+
Url:            http://fuse.sourceforge.net/
Group:          System Environment/Base
Source0:        https://github.com/libfuse/libfuse/archive/%{name}-%{version}.tar.gz
BuildRequires:  meson >= 0.38.0
BuildRequires:  %{python3_pkgprefix}-pytest
BuildRequires:  systemd-devel

%description
With FUSE3 it is possible to implement a fully functional filesystem in a
userspace program.

%package        devel
Summary:        Header and development files
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       systemd-devel

%description    devel
It contains the libraries and header files to create fuse applications.

%prep
%setup -q -n libfuse-%{name}-%{version}

%build
mkdir build &&
cd    build &&
meson --prefix=%{_prefix} .. &&
ninja-build -C ./

%install
cd build
DESTDIR=%{buildroot}/ ninja-build -C ./ install

%check
cd build
%{__python3} -m pytest test/

%files
%defattr(-, root, root)
%{_libdir}/libfuse3.so*
/usr/lib/udev/rules.d/*
%{_bindir}/*
%{_sysconfdir}/fuse*
%{_datadir}/man/*
%{_sbindir}/mount.fuse3
%exclude %{_sysconfdir}/init.d/fuse3

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/fuse3.pc
%{_libdir}/libfuse3.so*

%changelog
*   Thu Nov 29 2018 Stephane Thiell <sthiell@stanford.edu> 3.2.6-2
-   Made changes to build on CentOS 7.5
*   Mon Sep 24 2018 Srinidhi Rao <srinidhir@vmware.com> 3.2.6-1
-   Update to version 3.2.6.
*   Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.0.1-2
-   Move pkgconfig folder to devel package.
*   Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 3.0.1-1
-   Initial version.
