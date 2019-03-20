# Go build id is not supported for now.
# https://github.com/rpm-software-management/rpm/issues/367
# https://bugzilla.redhat.com/show_bug.cgi?id=1295951
%undefine _missing_build_ids_terminate_build

%global provider        github
%global provider_tld    com
%global project         Percona
%global repo            qan-api2
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          376dbed06e403faad1b444f99ab3e1e28ac7687e
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")

Name:           percona-qan-api2
Version:        2.0.0
Release:        4.%{build_timestamp}.%{shortcommit}%{?dist}
Summary:        Query Analytics API v2 for PMM

License:        AGPLv3
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:        %{name}.service

BuildRequires:  golang
Requires:       perl

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%description
Percona Query Analytics (QAN) API v2 is part of Percona Monitoring and Management.
See the PMM docs for more information.


%prep
%setup -T -c -n %{repo}-%{version}
%setup -q -c -a 0 -n %{repo}-%{version}
mkdir -p src/%{provider}.%{provider_tld}/%{project}
mv %{repo}-%{commit} src/%{provider_prefix}


%build
export GOPATH=$(pwd)
export APP_VERSION="%{version}-%{build_timestamp}.%{shortcommit}"
go build -o ./percona-qan-api2 -ldflags "-X main.version=${APP_VERSION}" ./src/%{provider_prefix}/*.go


%install
install -d -p %{buildroot}%{_sbindir}
mv ./percona-qan-api2 %{buildroot}%{_sbindir}/%{name}

install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service

%post
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_post %{name}.service
%endif

%preun
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_preun %{name}.service
%endif

%postun
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_postun %{name}.service
%endif


%files
#%license src/%{provider_prefix}/LICENSE
#%doc src/%{provider_prefix}/README.md src/%{provider_prefix}/CHANGELOG.md
%attr(0755, root, root) %{_sbindir}/%{name}
/usr/lib/systemd/system/%{name}.service

%changelog
* Tue Mar 19 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 2.0.0-4
- PMM-3681 Remove old qan-api and move qan-api2 in feature builds.

* Wed Dec 19 2018 Andrii Skomorokhov <andrii.skomorokhov@percona.com> - 2.0.0-1
- Initial.