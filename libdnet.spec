#
# Conditional build:
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module
%bcond_without	static_libs	# static library
#
Summary:	Interface to several low-level networking routines
Summary(pl.UTF-8):	Interfejs do niektórych niskopoziomowych funkcji sieciowych
Name:		libdnet
Version:	1.18.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/ofalk/libdnet/releases
Source0:	https://github.com/ofalk/libdnet/archive/libdnet-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5215b66fee62f0d52a8a74de5312abc3
Patch1:		%{name}-vlan.patch
Patch2:		%{name}-ip6.patch
URL:		https://github.com/ofalk/libdnet
BuildRequires:	autoconf >= 2.71
BuildRequires:	automake
BuildRequires:	libtool >= 2:2.2
%if %{with python2}
BuildRequires:	python-Cython
BuildRequires:	python-devel >= 1:2.7
%endif
%if %{with python3}
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 1:3.2
%endif
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libdnet provides a simplified, portable interface to several low-level
networking routines, including:
* network address manipulation
* kernel arp cache and route table lookup and manipulation
* network firewalling (IP filter, ipfw, ipchains, pf, ...)
* network interface lookup and manipulation
* raw IP packet and Ethernet frame transmission

%description -l pl.UTF-8
libdnet zapewnia uproszczony, przenośny interfejs do niektórych
niskopoziomowych funkcji sieciowych, włączając w to:
* manipulację adresami sieciowymi
* przeglądanie i modyfikację pamięci podręcznej ARP oraz tablic
  routingu
* firewalling (IP filter, ipfw, ipchains, pf, ...)
* wysyłanie ,,surowych'' pakietów IP i ramek Ethernetowych

%package devel
Summary:	Header files for libdnet
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libdnet
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libdnet.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libdnet.

%package static
Summary:	libdnet static library
Summary(pl.UTF-8):	Statyczna biblioteka libdnet
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
libdnet static library.

%description static -l pl.UTF-8
Statyczna biblioteka libdnet.

%package progs
Summary:	Sample applications to use with libdnet
Summary(pl.UTF-8):	Przykładowe aplikacje do wykorzystania libdnet
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description progs
Sample applications to use with libdnet.

%description progs -l pl.UTF-8
Przykładowe aplikacje do wykorzystania libdnet.

%package -n python-libdnet
Summary:	dnet Python 2 module
Summary(pl.UTF-8):	Moduł dnet dla Pythona 2
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-libdnet
dnet Python module.

%description -n python-libdnet -l pl.UTF-8
Moduł dnet dla Pythona.

%package -n python3-libdnet
Summary:	dnet Python 3 module
Summary(pl.UTF-8):	Moduł dnet dla Pythona 3
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python3-libdnet
dnet Python module.

%description -n python3-libdnet -l pl.UTF-8
Moduł dnet dla Pythona.

%prep
%setup -q -n %{name}-libdnet-%{version}
%patch -P1 -p1
%patch -P2 -p1

# invalid lvalues, force regeneration from .pyx
%{__rm} python/dnet.c

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	--without-python

%{__make}

cd python
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd python
%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md THANKS TODO
%attr(755,root,root) %{_libdir}/libdnet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdnet.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dnet-config
%attr(755,root,root) %{_libdir}/libdnet.so
%{_libdir}/libdnet.la
%{_includedir}/dnet
%{_includedir}/dnet.h
%{_mandir}/man3/dnet.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdnet.a
%endif

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dnet
%{_mandir}/man8/dnet.8*

%if %{with python2}
%files -n python-libdnet
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/dnet.so
%{py_sitedir}/dnet-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-libdnet
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/dnet.cpython-*.so
%{py3_sitedir}/dnet-%{version}-py*.egg-info
%endif
