# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 1
# Build project from bundled dependencies
%global with_bundled 0
# Build with debug info rpm
%global with_debug 0
# Run tests in check section
# Failing tests on various archs
%global with_check 0
# Generate unit-test rpm
%global with_unit_test 1

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         go-fsnotify
%global repo            fsnotify
# https://github.com/go-fsnotify/fsnotify
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global sec_import_path github.com/fsnotify/fsnotify
%global commit          f12c6236fe7b5cf6bcf30e5935d08cb079d78334
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global gopkg_import_path     gopkg.in/fsnotify.v1
%global sec_gopkg_import_path gopkg.in/v1/fsnotify

Name:           golang-%{provider}-%{project}-%{repo}
Version:        1.3.1
Release:        0.5.git%{shortcommit}%{?dist}
Summary:        File system notifications for Go
License:        BSD
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check}
BuildRequires: golang(golang.org/x/sys/unix)
%endif

Requires:      golang(golang.org/x/sys/unix)

Provides:      golang(%{import_path}) = %{version}-%{release}
Provides:      golang(%{sec_import_path}) = %{version}-%{release}
Provides:      golang(%{gopkg_import_path}) = %{version}-%{release}
Provides:      golang(%{sec_gopkg_import_path}) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path}, %{gopkg_import_path} and
%{sec_gopkg_import_path} prefix.

%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test
Summary:         Unit tests for %{name} package

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build

%install
# source codes for building projects
%if 0%{?with_devel}

install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
install -d -p %{buildroot}/%{gopath}/src/%{sec_import_path}/
echo "%%dir %%{gopath}/src/%%{sec_import_path}/." >> devel.file-list
install -d -p %{buildroot}/%{gopath}/src/%{gopkg_import_path}/
echo "%%dir %%{gopath}/src/%%{gopkg_import_path}/." >> devel.file-list
install -d -p %{buildroot}/%{gopath}/src/%{sec_gopkg_import_path}/
echo "%%dir %%{gopath}/src/%%{sec_gopkg_import_path}/." >> devel.file-list

# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    echo "%%dir %%{gopath}/src/%%{sec_import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{sec_import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{sec_import_path}/$file
    echo "%%{gopath}/src/%%{sec_import_path}/$file" >> devel.file-list

    echo "%%dir %%{gopath}/src/%%{gopkg_import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{gopkg_import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{gopkg_import_path}/$file
    echo "%%{gopath}/src/%%{gopkg_import_path}/$file" >> devel.file-list

    echo "%%dir %%{gopath}/src/%%{sec_gopkg_import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{sec_gopkg_import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{sec_gopkg_import_path}/$file
    echo "%%{gopath}/src/%%{sec_gopkg_import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc CHANGELOG.md README.md CONTRIBUTING.md AUTHORS
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test -f unit-test.file-list
%license LICENSE
%endif

%changelog
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-0.5.gitf12c623
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-0.4.gitf12c623
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-0.3.gitf12c623
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-0.2.gitf12c623
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.3.1-0.1.gitf12c623
- Bump to upstream f12c6236fe7b5cf6bcf30e5935d08cb079d78334
  related: #1318299

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.5.git96c060f
- https://fedoraproject.org/wiki/Changes/golang1.7

* Wed Mar 16 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.4.git96c060f
- Fix devel subpackage for gopkg.in
  resolves: #1318299

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.3.git96c060f
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-0.2.git96c060f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 11 2015 jchaloup <jchaloup@redhat.com> - 0-0.1.git96c060f
- First package for Fedora
  resolves: #1262426

