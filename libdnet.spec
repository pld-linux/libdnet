Summary:	interface to several low-level networking routines
Summary(pl):	interfejs do niektórych niskopoziomowych funkcji sieciowych
Name:		libdnet
Version:	1.7
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/libdnet/%{name}-%{version}.tar.gz
Patch0:		%{name}-am.patch
Patch1:		%{name}-lt.patch
URL:		http://libdnet.sourceforge.net/
BuildRequires:	autoconf
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

%description -l pl
libdnet zapewnia uproszczony, przeno¶ny interfejs do niektórych
niskopoziomowych funkcji sieciowych, w³±czaj±c w to:
* manipulacjê adresami sieciowymi
* przegl±danie i modyfikacjê pamiêci podrêcznej ARP oraz tablic routingu
* firewalling (IP filter, ipfw, ipchains, pf, ...)
* wysy³anie ,,surowych'' pakietów IP i ramek Ethernetowych

%package devel
Summary:	header files for libdnet
Summary(pl):	pliki nag³ówkowe libdnet
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for libdnet.

%description devel -l pl
Pliki nag³ówkowe libdnet.

%package static
Summary:	libdnet static library
Summary(pl):	statyczna biblioteka libdnet
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
libdnet static library.

%description static -l pl
Statyczna biblioteka libdnet.

%package progs
Summary:	sample applications to use with libdnet
Summary(pl):	przyk³adowe aplikacje do wykorzystania libdnet
Group:		Applications/Networking
Requires:	%{name} = %{version}

%description progs
Sample applications to use with libdnet.

%description progs -l pl
Przyk³adowe aplikacje do wykorzystania libdnet.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc THANKS TODO
%attr(755,root,root) %{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*-config
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.la
%{_includedir}/dnet
%{_includedir}/*.h
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
