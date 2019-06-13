%undefine _missing_build_ids_terminate_build
%global _dwz_low_mem_die_limit 0

%global provider	github
%global provider_tld	com
%global project		percona
%global repo		pmm-managed
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		8f3d007617941033867aea6a134c48b39142427f
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")
%define release         6
%define rpm_release     %{release}.%{build_timestamp}.%{shortcommit}%{?dist}

%define full_pmm_version 2.0.0

Name:		%{repo}
Version:	%{version}
Release:	%{rpm_release}
Summary:	Percona Monitoring and Management management daemon

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:        pmm-managed.service

BuildRequires:	golang

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%description
pmm-managed manages configuration of PMM server components (Prometheus,
Grafana, etc.) and exposes API for that.  Those APIs are used by pmm-admin tool.
See the PMM docs for more information.


%prep
%setup -q -n %{repo}-%{commit}
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(pwd) src/%{provider_prefix}


%build
export GOPATH=$(pwd)/

export PMM_RELEASE_VERSION=%{full_pmm_version}
export PMM_RELEASE_FULLCOMMIT=%{commit}
export PMM_RELEASE_BRANCH=""

cd src/github.com/percona/pmm-managed
# FIXME TODO HACK
env PMM_RELEASE_VERSION=2.0.0-beta2 make release


%install
install -d -p %{buildroot}%{_bindir}
install -d -p %{buildroot}%{_sbindir}
install -p -m 0755 bin/pmm-managed %{buildroot}%{_sbindir}/pmm-managed

install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service


%files
%license src/%{provider_prefix}/LICENSE
%doc src/%{provider_prefix}/README.md
%{_sbindir}/pmm-managed
/usr/lib/systemd/system/%{name}.service


%changelog
* Thu Sep 21 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.3.0-2
- add consul dependency for pmm-managed

* Tue Sep 12 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.3.0-1
- init version
