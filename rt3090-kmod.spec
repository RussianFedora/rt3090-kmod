# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#define buildforkernels newest

%define src_folder_name *RT3090*Linux*STA*

Name:		rt3090-kmod
Version:	2.4.0.4
Release:	3%{?dist}.4.R
Summary:	Kernel module for wireless devices with Ralink's RT3090 PCIe (RT3090) chipsets

Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://www.ralinktech.com/support.php?s=2
# No direct links anymore. The sources are downloaded from the above page.
Source0:	2010_1217_RT3090_LinuxSTA_V2.4.0.4_WiFiBTCombo_DPO.zip
Source11:	rt3090-kmodtool-excludekernel-filterfile
Patch0:		rt3090-fix-2860-conflicts.patch
Patch1:		no-tftpboot.patch
Patch2:		rt3090-Makefile.x-fixes.patch
Patch3:		rt3090-disable-cfg80211.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	%{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the documentation and configuration files for the Ralink
Driver for WiFi, a linux device driver for 802.11a/b/g universal NIC cards - 
either PCI, PCIe or MiniPCI - that use Ralink RT3090 PCIe 
(RT3090) chipsets.

%prep
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0
pushd %{src_folder_name}
%patch0 -p1 -b .CHIPSET_DAT
%patch1 -p1 -b .no24
%patch2 -p1 -b .rpmbuild
%patch3 -p1 -b .disable-cfg80211
popd

# Fix permissions
for ext in c h; do
 find . -name "*.$ext" -exec chmod -x '{}' \;
done

for kernel_version in %{?kernel_versions} ; do
 cp -a %{src_folder_name} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 make -C _kmod_build_${kernel_version%%___*} LINUX_SRC="${kernel_version##*___}"
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 make -C _kmod_build_${kernel_version%%___*} KERNELPATH="${kernel_version##*___}" KERNELRELEASE="${kernel_version%%___*}" INST_DIR=${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} install
done

chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/*
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Aug  2 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.4.0.4-3.4.R
- rebuilt

* Thu Jul 28 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.4.0.4-3.3.R
- rebuilt

* Tue Jul  5 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.4.0.4-3.2.R
- rebuilt

* Sun Apr 24 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.4.0.4-3.1.R
- rebuilt against new kernel

* Fri Feb 11 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.4.0.4-3
- update for new kernel

* Tue Jan 18 2011 Alexei Panov <elemc [AT] atisserv [DOT] ru> - 2.4.0.4-2
- Fix patches

* Mon Jan 17 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.4.0.4-1
- changed for RT3090 sources from rt2870-kmod package

* Sun Jan 16 2011 Alexei Panov <elemc [AT] atisserv [DOT] ru> - 2.4.1.1-1
- changed for RT3062 sources from rt2870-kmod package

* Fri Oct 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.4.0.1-1.1
- rebuild for F-14 kernel

* Sat Jul 10 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.4.0.1-1                                                                                                                                                        
- Update to 2.4.0.1

* Sun Jul 04 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.4.0.0-2
- Compilation fix against kernel >= 2.6.34

* Sat Jun 26 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.4.0.0-1
- Update to 2.4.0.0

* Sat Nov 28 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-6
- Add support for bunch of other devices. The device ID's are taken from rt2x00
  branch of kernel.

* Sat Nov 21 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-5
- No need to build i586 kmod anymore

* Sat Nov 21 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-4
- Add Hawking HWDN2 REV-E support

* Tue Nov 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.6
- rebuild for F12 release kernel

* Mon Nov 09 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.5
- rebuild for new kernels

* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.4
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.3
- rebuild for new kernels

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.2
- rebuild for new kernels

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.1
- rebuild for new kernels

* Sat Aug 22 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-3
- Suppress a flood of system log messages

* Mon Aug 03 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-2
- Fix for kernels >= 2.6.31

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.3
- rebuild for final F11 kernel

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.2
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.1
- rebuild for new kernels

* Fri May 22 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-1
- version update (2.1.2.0)

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.5
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.4
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.3
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.2
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.1
- rebuild for new kernels

* Sat Apr 24 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-1
- version update (2.1.1.0)

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.0.0-2.1
- rebuild for new kernels

* Thu Mar 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.0.0-2
- Bugfix: kmod doesn't compile when the kernel version has a "2.4" substring

* Thu Mar 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.0.0-1
- New upstream version
- Drop additional-devices patch since it is upstreamed

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-7.1
- rebuild for latest Fedora kernel;

* Wed Feb 11 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-7
- Add Sweex WL303 support

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-6.1
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-6
- Add Belkin F5D8053 support

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-5.2
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-5.1
- rebuild for latest Fedora kernel;

* Thu Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-5
- Add Buffalo WLI-UC-G300N support

* Sun Jan 11 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-4
- Add a patch for compilation against kernels >= 2.6.29

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-3.4
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-3.3
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-3.2
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-3.1
- rebuild for latest Fedora kernel;

* Wed Dec 17 2008 Jarod Wilson <jarod@wilsonet.com> - 1.4.0.0-3
- Add device ID for Linksys WUSB600N

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-2.1
- rebuild for latest Fedora kernel;

* Thu Dec 04 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-2
- removed the iwe-stream patch since it is not needed for 2.6.27+ kernels

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.9
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.8
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.7
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.6
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.5
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.4
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.3
- rebuild for latest rawhide kernel; enable ppc and ppc64 again

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.2
- rebuild for latest rawhide kernel

* Sun Oct 05 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.4.0.0-1.1
- adjust make call in build to build properly is running kernel and target
  kernel are different

* Sat Oct 04 2008  Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-1
- Rebuild for 1.4.0.0

* Sat Oct 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.3.1.0-4
- Various small adjustments
- exclude ppc due to bugs (see comments)

* Sat Sep 26 2008  Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.3.1.0-3
- Re-wrote the description, removed supported hardware info. 
- Renamed SourceDir to SourceName

* Thu Sep 22 2008  Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.3.1.0-2
- Some cleanup in the SPEC file to match standards
- Separated the patches
- License is GPLv2+

* Thu Sep 20 2008  Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.3.1.0-1
- Initial build. The patch fixes compilation problems for kernels >= 2.6.25 . Also adds support for Linksys WUSB100.
