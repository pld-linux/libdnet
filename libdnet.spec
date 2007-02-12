# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Interface to several low-level networking routines
Summary(pl.UTF-8):   Interfejs do niektórych niskopoziomowych funkcji sieciowych
Name:		libdnet
Version:	1.8
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/libdnet/%{name}-%{version}.tar.gz
# Source0-md5:	187054990cd8e4e1aa6845912b34236d
Patch0:		%{name}-ac.patch
Patch1:		%{name}-am.patch
URL:		http://libdnet.sourceforge.net/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	libtool
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
* przeglądanie i modyfikację pamięci podręcznej ARP oraz tablic routingu
* firewalling (IP filter, ipfw, ipchains, pf, ...)
* wysyłanie ,,surowych'' pakietów IP i ramek Ethernetowych

%package devel
Summary:	Header files for libdnet
Summary(pl.UTF-8):   Pliki nagłówkowe biblioteki libdnet
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libdnet.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libdnet.

%package static
Summary:	libdnet static library
Summary(pl.UTF-8):   Statyczna biblioteka libdnet
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
libdnet static library.

%description static -l pl.UTF-8
Statyczna biblioteka libdnet.

%package progs
Summary:	Sample applications to use with libdnet
Summary(pl.UTF-8):   Przykładowe aplikacje do wykorzystania libdnet
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description progs
Sample applications to use with libdnet.

%description progs -l pl.UTF-8
Przykładowe aplikacje do wykorzystania libdnet.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
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
%doc THANKS TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/dnet
%{_includedir}/*.h
%{_mandir}/man3/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
