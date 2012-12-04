Name: kde-plasma-alsa-volume
Version: 0.40.2
Release: 1%{?dist}
Summary: ALSA Volume Control plasmoid.
Summary(ru): Плазмоид для управления ALSA устройствами.
Group: Applications/Multimedia
License: GPLv2+
Source0: http://cloud.github.com/downloads/F1ash/plasmaVolume/%{name}-%{version}.tar.bz2
URL: https://github.com/F1ash/plasmaVolume
BuildArch: noarch

Requires: PyKDE4, python-alsaaudio

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

* Tue Dec 05 2012 Fl@sh <kaperang07@gmail.com> - 0.40.2-1
- version update

* Thu Sep 29 2011 Fl@sh <kaperang07@gmail.com> - 0.38.2-5
- selected stable method of wait thread run

* Tue Sep 27 2011 Fl@sh <kaperang07@gmail.com> - 0.38.1-5
- added python-alsaaudio requires in spec

* Mon Aug 29 2011 Fl@sh <kaperang07@gmail.com> - 0.38.1-3
- fixed Makefile

* Mon Aug 29 2011 Fl@sh <kaperang07@gmail.com> - 0.38.1-2
- fixed Makefile

* Mon Aug 22 2011 Fl@sh <kaperang07@gmail.com> - 0.38.1-1
- Initial build
