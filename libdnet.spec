#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Interface to several low-level networking routines
Summary(pl.UTF-8):	Interfejs do niektórych niskopoziomowych funkcji sieciowych
Name:		libdnet
Version:	1.12
Release:	4
License:	BSD
Group:		Libraries
#Source0Download: https://code.google.com/p/libdnet/downloads/list
Source0:	https://libdnet.googlecode.com/files/%{name}-%{version}.tgz
# Source0-md5:	9253ef6de1b5e28e9c9a62b882e44cc9
Patch0:		%{name}-python.patch
Patch1:		%{name}-vlan.patch
Patch2:		%{name}-ip6.patch
URL:		https://code.google.com/p/libdnet/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	python-Pyrex
BuildRequires:	python-devel >= 1:2.5
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
Summary:	libdnet Python module
Summary(pl.UTF-8):	Moduł libdnet dla Pythona
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-libdnet
libdnet Python module.

%description -n python-libdnet -l pl.UTF-8
Moduł libdnet dla Pythona.

%prep
%setup -q
%patch -P0 -p1
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
	--with-python \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README THANKS TODO
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

%files -n python-libdnet
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/dnet.so
%{py_sitedir}/dnet-%{version}-py*.egg-info
