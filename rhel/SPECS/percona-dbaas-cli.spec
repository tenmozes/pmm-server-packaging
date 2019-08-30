%global _dwz_low_mem_die_limit 0

%global provider	github
%global provider_tld	com
%global project		Parcona-Lab
%global repo		percona-dbaas-cli
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		16241617f6758d82105ac20793b98a92139254b6
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")
%define release         6
%define rpm_release     %{release}.%{build_timestamp}.%{shortcommit}%{?dist}
%undefine _missing_build_ids_terminate_build

Name:		%{repo}
Version:	%{version}
Release:	%{rpm_release}
Summary:	Percona DBAAS cli.

License:	ASL 2.0
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildRequires:	golang

%description
percona-dbaas-cli
See the PMM docs for more information.


%prep
%setup -q -n %{repo}-%{commit}
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(pwd) src/%{provider_prefix}


%build
go build -o percona-dbaas-cli ./cmd/percona-dbaas


%install
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 percona-dbaas-cli %{buildroot}%{_bindir}/percona-dbaas-cli


%files
%license src/%{provider_prefix}/LICENSE
%{_bindir}/percona-dbaas-cli
