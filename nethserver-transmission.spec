%define name nethserver-transmission
%define version 1.1.14
%define release 2
Summary: transmission is a helpdesk system to download the Nethserver iso
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
URL: http://dev.nethserver.org/projects/nethforge/wiki/%{name} 
Distribution: nethserver
License: GNU GPL version 2
Group: Neth/addon
Source: %{name}-%{version}.tar.gz
BuildArchitectures: noarch
BuildRoot: /var/tmp/%{name}-%{version}-buildroot
BuildRequires: nethserver-devtools
Requires: nethserver-ibays nethserver-samba nethserver-httpd
Requires: mod_authnz_pam
Requires: transmission-cli, transmission-common, transmission-daemon
AutoReqProv: no

%description
transmission is an application adapted as a contrib for nethserver, to help the  seeding of the Nethserver CDROM ISO. 


%prep
%setup

%build
%{makedocs}
perl createlinks
%{__mkdir_p} root/var/lib/transmission/Downloads
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf $RPM_BUILD_ROOT
(cd root ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
cp -a manifest.json %{buildroot}/usr/share/cockpit/%{name}/
cp -a logo.png %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

rm -f %{name}-%{version}-filelist
%{genfilelist} \
    --dir /var/lib/transmission/Downloads 'attr(0775,transmission,transmission)' \
 $RPM_BUILD_ROOT \
     > %{name}-%{version}-filelist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)

%dir %{_nseventsdir}/%{name}-update
%pre

%post

%postun
if [ $1 == 0 ] ; then
    /usr/bin/rm -f /etc/httpd/conf.d/transmission-daemon.conf
    /usr/bin/rm -f /etc/httpd/conf.d/transmission-WebDL.conf
    /usr/bin/systemctl reload httpd
fi

%changelog
* Fri Jun 11 2021 stephane de Labrusse <stephdl@de-labrusse.fr> 1.1.14
- Split with comma in templates
- Use same users for smb and web

* Sun Jul 05 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 1.1.13
- Remove http templates after rpm removal

* Tue Oct 15 2019 Stephane de Labrusse <stephdl@de-labrusse.fr> 1.1.11-1.ns7
- cockpit. added to legacy apps

* Wed Mar 13 2019 stephane de Labrusse <stephdl@de-labrusse.fr> 1.1.10-1.ns7
- specific repository for transmission

* Mon Mar 11 2019 stephane de Labrusse <stephdl@de-labrusse.fr> 1.1.9-1.ns7
- Action to push configuration to json file
- Added rpc-host-whitelist values in json file
- added definition of geekery.repo

* Fri Oct 12 2018 stephane de labrusse <stephdl@de-labrusse.fr> 1.1.8-1.ns7
- Subscribe to the nethserver-sssd-save event

* Mon Aug 13 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> 1.1.7-1.ns7
- The transmission dependency is removed, no GTK needs
- Thanks to Mark Verlinde markVnl

* Wed Jan 10 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> 1.1.6-1.ns7
- Open the peer port directly in shorewall

* Sun Nov 12 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> 1.1.5-1.ns7
- user name validation

* Sun Sep 10 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> 1.1.4-1.ns7
- Restart httpd service on trusted-network

* Wed Mar 29 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> 1.1.3-1.ns7
- Template expansion on trusted-network

* Wed Mar 15 2017 Stephane de Labrusse  <stephdl@de-labrusse.fr> 1.1.2-1.ns7
- Use samba guest access, even if nethserver-directory is not installed

* Mon Feb 06 2017 Stephane de Labrusse  <stephdl@de-labrusse.fr> 1.1.1-2.ns7
- Force all transmission dependencies in this spec file

* Wed Nov 23 2016 Stephane de Labrusse  <stephdl@de-labrusse.fr> 1.1.1-1.ns7
- A watched directory is now created for torrent file

* Mon Nov 21 2016 Stephane de Labrusse  <stephdl@de-labrusse.fr> 1.1.0-2
- Samba guest access allowed when ldap is the account provider

* Fri Nov 18 2016 Stephane de Labrusse  <stephdl@de-labrusse.fr> 1.1.0-1
- NS7 version

* Fri May 15 2015 Stephane de Labrusse  <stephdl@de-labrusse.fr> 1.0.1-2
- now transmission key is set as a 'configuration' type

* Sun May 10 2015 Stephane de Labrusse  <stephdl@de-labrusse.fr> 1.0.1-1
- Initial release to Nethserver

* Fri Dec 27 2014 Stephane de Labrusse  <stephdl@de-labrusse.fr> 0.0.3-1
- corrected array issues in templated configuration files [SME: 8749]
- corrected the path of unixgroup to /usr/bin/unixgroup

* Mon May 12 2014 Stéphane de Labrusse  <stephdl@de-labrusse.fr> 0.0.2-1
- removed the post-upgrade from template2expand

* Sun Nov 17 2013  Stéphane de Labrusse  <stephdl@de-labrusse.fr> 0.0.1-9
- add folder /var/lib/transmission/Downloads to avoid log errors
- add a db command to choose the location of transmission download folder
* Sat Nov 16 2013  Stéphane de Labrusse  <stephdl@de-labrusse.fr> 0.0.1-6
- final release
* Fri Nov 15 2013  Stéphane de Labrusse <stephdl@de-labrusse.fr> 0.0.1-3
- Modified smeserver templates (settings.json,61transmission-reverse-proxy)
- Add a web folder to download torrent https://sme-ip/transmission-dl
* Tue Nov 12 2013  Stéphane de Labrusse <stephdl@de-labrusse.fr> 0.0.12
- The work continue
* Sat Nov 09 2013  CONTRIB MAKER <tests@pialasse.com> 0.0.1-1.sme
- initial release
- builds from unchanged .tar.gz 
