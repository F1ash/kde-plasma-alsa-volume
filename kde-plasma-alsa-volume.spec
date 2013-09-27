Name: kde-plasma-alsa-volume
Version: 0.51.0
Release: 1%{?dist}
Summary: ALSA Volume Control plasmoid
Summary(ru): Плазмоид для управления ALSA устройствами
License: GPLv2+
Source0: https://github.com/F1ash/%{name}/archive/%{version}.tar.gz
URL: https://github.com/F1ash/%{name}
BuildArch: noarch

Requires: python-alsaaudio
BuildRequires: kdelibs4-devel

%description
%{name}
ALSA Volume Control plasmoid.
This plasmoid is very convenient, because it allows to each device
be reflected on the panel (or workspace) for control.
It can to detect the multiple audiodevices (audiocards) in system.

%description -l ru
%{name}
Плазмоид для управления ALSA устройствами.
Позволяет отражать для управления каждое устройство в панели
или рабочем пространстве. Может определять несколько аудио-карт
в системе.

%prep
%setup -q

%build
if [ -x %{_bindir}/plasma-dataengine-depextractor ] ; then
  plasma-dataengine-depextractor .
fi
make %{?_smp_mflags}

%install
%{make_install}

%files
%{_kde4_datadir}/kde4/services/%{name}.desktop
%{_kde4_appsdir}/plasma/plasmoids/%{name}
%doc README COPYING Changelog

%changelog
* Fri Sep 27 2013 Fl@sh <kaperang07@gmail.com> - 0.51.0-1
- version update

* Thu Sep 19 2013 Fl@sh <kaperang07@gmail.com> - 0.50.0-1
- spec simplified;
- version update

* Mon Jul 01 2013 Fl@sh <kaperang07@gmail.com> - 0.43.5-1
- version update

* Thu Jun 06 2013 Fl@sh <kaperang07@gmail.com> - 0.42.3-1
- version update

* Tue Apr 02 2013 Fl@sh <kaperang07@gmail.com> - 0.42.2-1
- version update

* Wed Dec 06 2012 Fl@sh <kaperang07@gmail.com> - 0.41.2-1
- version update
- added docs-files & fixed files path
- added plasma-dataengine-depextractor approach

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
