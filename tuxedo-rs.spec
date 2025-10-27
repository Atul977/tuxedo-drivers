%global gui_name tailor-gui
%global branch_name main
%global datestamp %(date +%Y%m%d)

Name:           tailord
Version:        0.2.5
Summary:        System daemon for TUXEDO hardware control
Release:        0.1.%{datestamp}%{?dist}
License:        GPL-2.0-or-later
URL:            https://github.com/AaronErhardt/tuxedo-rs/
Source0:        %{url}/archive/refs/heads/%{branch_name}.tar.gz#/%{name}-%{branch_name}.tar.gz

BuildRequires:  meson pkgconfig(systemd) desktop-file-utils libappstream-glib-devel
BuildRequires:  pkgconfig(libadwaita-1) pkgconfig(gtk4) cargo rust-srpm-macros gcc systemd-rpm-macros
Requires:       tuxedo-drivers

%package -n %{gui_name}
Summary:        Graphical client for the %{name} daemon
Requires:       %{name} = %{version}-%{release} gtk4 libadwaita

%description
This package contains the %{name} system service, which provides the D-Bus
interface for controlling TUXEDO hardware.

%description -n %{gui_name}
This package provides the graphical Gtk4 client for the %{name} service.

%prep
%autosetup -n tuxedo-rs-%{branch_name}
sed -e 's|ExecStart=.*|ExecStart=%{_bindir}/%{name}|' %{name}/%{name}.service.in > %{name}.service

%build
pushd %{name}
%meson
%meson_build
popd

pushd tailor_gui
%meson
%meson_build
popd

%install
install -Dm0755 %{name}/redhat-linux-build/src/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm0644 %{name}/com.tux.Tailor.conf %{buildroot}%{_datadir}/dbus-1/system.d/com.tux.Tailor.conf
install -Dm0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service

pushd tailor_gui
%meson_install
popd

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md %{name}/CHANGELOG.md
%{_bindir}/%{name}
%{_datadir}/dbus-1/system.d/com.tux.Tailor.conf
%{_unitdir}/%{name}.service

%files -n %{gui_name}
%{_bindir}/tailor_gui
%{_datadir}/applications/com.github.aaronerhardt.Tailor.desktop
%{_datadir}/metainfo/com.github.aaronerhardt.Tailor.metainfo.xml
%{_datadir}/tailor_gui/resources.gresource
%{_datadir}/glib-2.0/schemas/com.github.aaronerhardt.Tailor.gschema.xml
%{_datadir}/icons/hicolor/

%changelog
* %(date +"%a %b %d %Y") Your Name <youremail@example.com> - %{version}-0.1.%{datestamp}
- Nightly build from main branch
