Name:		snapper
Version:	0.1.7
Release:	10%{?dist}
License:	GPLv2
Group:		Applications/System
BuildRequires:	boost-devel gettext libtool libxml2-devel dbus-devel
BuildRequires:	pam-devel libxslt docbook-style-xsl btrfs-progs-devel >= 3.16.1
BuildRequires:	libselinux-devel libacl-devel
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	diffutils%{?_isa}
Summary:	Tool for filesystem snapshot management
Url:		http://en.opensuse.org/Portal:Snapper

Source0:	https://github.com/openSUSE/snapper/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
patch0:		%{name}-remove-ext4-info-xml.patch
patch1:		%{name}-rename-cron-files.patch
patch2:		%{name}-securelibdir.patch
patch3:		%{name}-0.1.8-adapt-to-libbtrfs-change.patch
patch4:		%{name}-0.2.1-btrfs-fix-internal-cmp.patch
patch5:		%{name}-manpages-remove-invalid-references.patch
patch6:		%{name}-0.2.2-add-norecovery-option-xfs.patch
patch7:		%{name}-0.2.2-fix-acl-revert-xfs.patch
patch8:		%{name}-add-selinux-restorecon-support.patch
patch9:		%{name}-0.2.2-fixed-empty-pre-post-cleanup-algorithm.patch
patch10:	%{name}-0.2.4-add-conditionals-for-btrfs-library-versions.patch
patch11:	%{name}-0.2.2-fixed-segmentation-fault-with-dbus.patch
patch12:	%{name}-0.2.8-move-refcounters.patch
patch13:	%{name}-0.2.8-get-files-by-pipe.patch
patch14:	%{name}-workaround-linkage-issue-on-some-archs.patch

%description
This package contains snapper, a tool for filesystem snapshot management.

%package libs
Summary:	Library for filesystem snapshot management
Group:		System Environment/Libraries
Requires:	util-linux%{?_isa} btrfs-progs%{?_isa} >= 3.16.1 libselinux%{?_isa}
Requires:	libacl%{?_isa}

%description libs
This package contains the snapper shared library
for filesystem snapshot management.

%package devel
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libstdc++-devel%{?_isa} boost-devel%{?_isa} libxml2-devel%{?_isa}
Summary:	Header files and documentation for libsnapper

%description devel
This package contains header files and documentation for developing with
snapper.

%package -n pam_snapper
Requires:	%{name}%{?_isa} = %version-%{release}
Requires:	pam%{?_isa}
Summary:	PAM module for calling snapper

%description -n pam_snapper
A PAM module for calling snapper during user login and logout.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%build
aclocal
libtoolize --force --automake --copy
autoheader
automake --add-missing --copy
autoconf
# NOTE: --disable-ext4 option removes support for ext4 internal snapshots since the feature
# never made it into upstream kernel
%configure --disable-silent-rules --disable-ext4 --docdir=%{_defaultdocdir}/%{name}-%{version} --disable-zypp --enable-selinux
#NOTE: avoid 'unused-direct-shlib-dependency' warning in rpmlint checks
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
install -m644 -D data/sysconfig.snapper %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{find_lang} %{name}
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_libdir}/security/*.la

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files -f snapper.lang
%{_bindir}/snapper
%{_sbindir}/snapperd
%config(noreplace) %{_sysconfdir}/logrotate.d/snapper
%{_sysconfdir}/cron.hourly/snapper
%{_sysconfdir}/cron.daily/snapper
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.opensuse.Snapper.conf
%{_datadir}/dbus-1/system-services/org.opensuse.Snapper.service
%doc AUTHORS
%{_mandir}/man8/%{name}.8*
%{_mandir}/man8/snapperd.8*
%{_mandir}/man5/snapper-configs.5*

%files libs
%{_libdir}/libsnapper.so.*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/configs
%dir %{_sysconfdir}/%{name}/config-templates
%config(noreplace) %{_sysconfdir}/%{name}/config-templates/default
%dir %{_sysconfdir}/%{name}/filters
%config(noreplace) %{_sysconfdir}/%{name}/filters/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%doc AUTHORS COPYING

%files devel
%doc examples/c/*.c
%doc examples/c++-lib/*.cc
%{_libdir}/libsnapper.so
%{_includedir}/%{name}

%files -n pam_snapper
#%defattr(-,root,root)
%{_libdir}/security/pam_snapper.so
%dir %{_prefix}/lib/pam_snapper
%{_prefix}/lib/pam_snapper/*.sh
%doc %{_mandir}/*/pam_snapper*.*

%changelog
* Wed Aug 05 2015 Ondrej Kozina <okozina@redhat.com> - 0.1.7-10
- patch: use pipe instead of socket pair for transfering large data
- Resolves: #1229353

* Thu Jul 30 2015 Ondrej Kozina <okozina@redhat.com> - 0.1.7-9
- patch: fix snapperd abort while passing large data over dbus
- patch: workaround linkage issue on s390 and ppc64le
- Resolves: #1229353

* Tue Jul 07 2015 Ondrej Kozina <okozina@redhat.com> - 0.1.7-8
- patch: fix segmentation fault with dbus
- Resolves: #1231684

* Mon Sep 29 2014 Ondrej Kozina <okozina@redhat.com> - 0.1.7-7
- patch: fix empty-pre-post cleanup algorithm
- patch: add conditionals for btrfs library versions
- Resolves: #1071973 #1142954

* Wed Feb 26 2014 Ondrej Kozina <okozina@redhat.com> - 0.1.7-6
- patch: Add norecovery option mounting XFS read-only snapshot
- patch: Fix ACL modification failure with XFS filesystem
- patch: Sync SELinux context of .snapshots subvolume (btrfs only)
- Resolves: #1064111, #1065969, #1069312

* Tue Feb 11 2014 Ondrej Kozina <okozina@redhat.com> - 0.1.7-5
- patch: Fix failure in invoking btrfs internal comparison of subvolumes
- patch: Remove references to missing programs from man pages
- Resolves: #1060806, #1063844

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.1.7-4
- Mass rebuild 2014-01-24

* Fri Jan 24 2014 Ondrej Kozina <okozina@redhat.com> - 0.1.7-3
- enable btrfs compare using send/receive in libbtrfs
- patch: adapt sources to change in libtrfs API (btrfs_read_and_process_send_stream)
- Resolves: #1055579

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.1.7-2
- Mass rebuild 2013-12-27

* Tue Oct 15 2013 Ondrej Kozina <okozina@redhat.com> - 0.1.7-1
- Update to snapper 0.1.7
- Resolves: #995102

* Mon Jul 29 2013 Ondrej Kozina <okozina@redhat.com> - 0.1.5-1
- updated to latest upstream
- allow whitespace in ALLOW_USERS and ALLOW_GROUPS in snapper's config
- enable new pam module
- patch: pam module installed in proper libdir

* Fri Apr 26 2013 Ondrej Kozina <okozina@redhat.com> - 0.1.3-1.20130426git35ff4ec
- fixed possible security vulnerability in extended attributes handling

* Thu Apr 18 2013 Ondrej Kozina <okozina@redhat.com> - 0.1.3-1.20130418git7ca81a2
- updatet to latest upstream version
- add support to compare extended attributes ('xadiff' command)
- add support to revert modificiations in file's extended attributes
- patch: avoid useless build dependency on libattr-devel

* Mon Feb 11 2013 Ondrej Kozina <okozina@redhat.com> - 0.1.2-1.20130211git676556f
- updated to latest upstream version
- fixed wrong include: "auto_ptr.h" -> <memory>
- moved diffutils dependency to client

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.1.0-2.20121026git1aaa372
- Rebuild for Boost-1.53.0

* Fri Oct 26 2012 Ondrej Kozina <okozina@redhat.com> - 0.1.0-1.20121026git1aaa372
- removed python binding since python can use dbus interface instead
- removed btrfs-progs and LVM dependecies (#852174)
- patch: do not build zypp plugin
- patch: avoid abrt when 'diff' command is executed without arguments
- patch: do not check for btrfs-progs binary
- patch: do not allow 'create-config' command on non-thin LVM volumes (#852174)
- edit libtool script to link with: '-Wl, --as-needed'
- spec file polishing

* Wed Sep 26 2012 Ondrej Kozina <okozina@redhat.com> - 0.0.14-3.20120926git7918e5c
- add dbus interface
- patch man page to reflect unsupported ext4 snapshots

* Wed Sep 5 2012 Ondrej Kozina <okozina@redhat.com> - 0.0.14-2.20120905gitb0d0145
- Rename cron files
- Fix multiple review notes issued in (#852174)

* Mon Aug 27 2012 Ondrej Kozina <okozina@redhat.com> - 0.0.14-1
- Initial build
