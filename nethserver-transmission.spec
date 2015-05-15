%define name nethserver-transmission
%define version 1.0.1
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
Requires: nethserver-ibays nethserver-samba nethserver-directory nethserver-httpd
Requires: pwauth mod_authnz_external
Requires: transmission >= 2.84
AutoReqProv: no

%description
transmission is an application adapted as a contrib for nethserver, to help the  seeding of the Nethserver CDROM ISO. 


%prep
%setup

%build
%{makedocs}
perl createlinks
%{__mkdir_p} root/var/lib/transmission/Downloads

%install
rm -rf $RPM_BUILD_ROOT
(cd root ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist \
    --dir /var/lib/transmission/Downloads 'attr(0775,transmission,transmission)' \
    --dir /var/lib/transmission 'attr(0775,transmission,transmission)' \
 $RPM_BUILD_ROOT \
     > %{name}-%{version}-filelist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)

%pre

%post

echo "
 Hi

 All my development work is done in my free time and from my own expenses. 
 If you consider my work as something helpful, thank you to kindly make 
 a donation to my paypal account and allow me to continue paying my server 
 and all associated costs.

 https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZPK8FKHVT4TY8

 Thank in advance.
 
 Stephane de Labrusse Alias Stephdl
"
%changelog
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
