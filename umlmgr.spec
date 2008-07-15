%define name umlmgr
%define version 0.10
%define release %mkrel 1

Summary: Uml manager
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires:    rpm-helper >= 0.16
BuildArch: noarch
BuildRequires: perl(Config::IniFiles)
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(Sys::Syslog)
BuildRequires: perl(IPC::Open3)
Requires(post):   rpm-helper >= 0.16
Requires(pre):   rpm-helper >= 0.16
Requires(postun): rpm-helper >= 0.16
Requires(preun): rpm-helper >= 0.16

%description 
Umlmgr is a set of script to automated and manage User Mode Linux
virtual Machines.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make

%check
%make test

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

install -D -m 644 etc/umlmgr.cfg %buildroot%_sysconfdir/umlmgr.cfg
install -D -m 755 etc/umlmgr.init %buildroot%_initrddir/umlmgr
install -d %buildroot%_sysconfdir/umlmgr
install -d %buildroot/var/lib/umlmgr/tmp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %_sysconfdir/umlmgr
%config(noreplace) %_sysconfdir/umlmgr.cfg
%_initrddir/umlmgr
%_bindir/*
%{perl_vendorlib}/*
%{_mandir}/*/*
%attr(0750, umlmgr, umlmgr) /var/lib/umlmgr

%pre
%_pre_useradd umlmgr /var/lib/umlmgr /bin/false

%postun
%_postun_userdel umlmgr
