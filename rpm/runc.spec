#
# spec file for package runc
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# nodebuginfo


# MANUAL: Make sure you update this each time you update runc.
%define git_version bc20cb4497af9af01bea4a8044f1678ffca2745c
%define git_short   bc20cb4497af

%define project github.com/opencontainers/runc

Name:           runc
Version:        1.2.5
Release:        1
Summary:        Tool for spawning and running OCI containers
License:        Apache-2.0
Group:          System/Management
URL:            https://github.com/opencontainers/runc
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  diffutils
BuildRequires:  fdupes
BuildRequires:  golang(API) >= 1.24
BuildRequires:  libseccomp-devel
BuildRequires:  libselinux-devel
Recommends:     criu
# There used to be a docker-runc package which was specifically for Docker.
# Since Docker now tracks upstream more consistently, we use the same package
# but we need to obsolete the old one. bsc#1181677
Obsoletes:      docker-runc < %{version}
Provides:       docker-runc = %{version}

%description
runc is a CLI tool for spawning and running containers according to the OCI
specification. It is designed to be as minimal as possible, and is the workhorse
of Docker. It was originally designed to be a replacement for LXC within Docker,
and has grown to become a separate project entirely.

%prep
%autosetup -n %{name}-%{version}/%{name}

%build
make BUILDTAGS="seccomp" COMMIT="%{git_describe}" runc

%install
# We install to /usr/sbin/runc as per upstream and create a symlink in /usr/bin
# for rootless tools.
install -D -m0755 %{name} %{buildroot}%{_sbindir}/%{name}
install -m0755 -d %{buildroot}%{_bindir}
ln -s  %{_sbindir}/%{name} %{buildroot}%{_bindir}/%{name}
cp LICENSE ../

%fdupes %{buildroot}

%files
%license LICENSE
%{_sbindir}/%{name}
%{_bindir}/%{name}

