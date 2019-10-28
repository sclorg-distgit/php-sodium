# centos/sclo spec file for php-sodium
#
# Copyright (c) 2018-2019 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix sclo-php73-
%scl_package        php-sodium
%else
%global pkg_name    %{name}
%endif

%global pecl_name  sodium
%global ini_name   20-%{pecl_name}.ini

Name:           %{?sub_prefix}php-%{pecl_name}
Summary:        Wrapper for the Sodium cryptographic library
Version:        7.3.7
Release:        1%{?dist}
Source0:        http://www.php.net/distributions/php-%{version}.tar.xz

License:        PHP
Group:          Development/Languages
URL:            http://php.net/%{pecl_name}

BuildRequires:  %{?scl_prefix}php-devel >= 7.3
BuildRequires:  libsodium-devel  >= 1.0.8

%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}php-%{pecl_name}          = %{version}-%{release}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}


%description
The %{name} package package provides a simple,
low-level PHP extension for the libsodium cryptographic library.


%prep
%setup -q -n php-%{version}

# Fix reported version
sed -e '/PHP_SODIUM_VERSION/s/PHP_VERSION/"%{version}"/' \
    -i ext/%{pecl_name}/php_libsodium.h

# Configuration file
cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%build
cd ext/%{pecl_name}

%{_bindir}/phpize
%configure \
    --with-sodium \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config

make %{?_smp_mflags}


%install
# Install the NTS stuff
make -C ext/%{pecl_name} install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}


%check
cd ext/%{pecl_name}

# can load the module
%{_bindir}/php -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}

# reported version from reflection
%{_bindir}/php -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --re %{pecl_name} | grep %{version}

# Upstream test suite
export NO_INTERACTION=1
export REPORT_EXIT_STATUS=1
make test 


%files
%license LICENSE
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so


%changelog
* Mon Oct 28 2019 Remi Collet <remi@remirepo.net> - 7.3.7-1
- update to 7.3.7 for sclo-php73

* Thu Nov 15 2018 Remi Collet <remi@remirepo.net> - 7.2.12-1
- version 7.2.12 for sclo-php72

