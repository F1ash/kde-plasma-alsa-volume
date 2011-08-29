Name: kde-plasma-alsa-volume
Version: 0.38.1
Release: 3%{?dist}
Summary: ALSA Volume Control plasmoid.
Summary(ru): Плазмоид для управления ALSA устройствами.
Group: Applications/Multimedia
License: GPL
Source0: http://cloud.github.com/downloads/F1ash/plasmaVolume/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: https://github.com/F1ash/plasmaVolume
BuildArch: noarch

Requires: python, PyQt4, PyKDE4

%description
kde-plasma-alsa-volume
ALSA Volume Control plasmoid.

%description -l ru
kde-plasma-alsa-volume
Плазмоид для управления ALSA устройствами.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT/usr

%files
%defattr(-,root,root)
%{_datadir}/kde4/services/%{name}.desktop
%{_datadir}/kde4/apps/plasma/plasmoids/%{name}/*
%dir %{_datadir}/kde4/apps/plasma/plasmoids/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Mon Aug 29 2011 Fl@sh <kaperang07@gmail.com> - 0.38.1-3
- fixed Makefile

* Mon Aug 29 2011 Fl@sh <kaperang07@gmail.com> - 0.38.1-2
- fixed Makefile

* Mon Aug 22 2011 Fl@sh <kaperang07@gmail.com> - 0.38.1-1
- Initial build
