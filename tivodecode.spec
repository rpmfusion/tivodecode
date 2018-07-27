Name:           tivodecode
Version:        0.2
Release:        0.10.pre4%{?dist}
Summary:        Convert a .TiVo file from TiVoToGo to a normal MPEG

Group:          Applications/Multimedia
# sha1.c is public domain, but resulting package is BSD and QUALCOMM
License:        BSD and QUALCOMM
URL:            http://tivodecode.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}pre4.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake, autoconf, libtool
Requires:       tivodecode-libs = %{version}-%{release}

%description
This software converts a .TiVo file (produced by the TiVoToGo functionality on
recent TiVo software releases) to a normal MPEG file. This has the same
functionality as using TiVo's supplied DirectShow DLL on Windows with a tool
such as DirectShowDump, but is portable to different architectures and
operating systems, and runs on the command line using files or pipes. The
conversion still requires the valid MAK of the TiVo which recorded the file,
so it cannot be used to circumvent their protection, simply to provide the
same level of access as is already available on Windows. 

%package libs
Summary:        A library to convert a TiVo data stream
Group:          System Environment/Libraries

%description libs
This package contains the library files for libtivodecode.

%package devel
Summary:        A library to convert a TiVo data stream
Group:          Development/Libraries
Requires:       tivodecode-libs = %{version}-%{release}

%description devel
This package contains the developer files for libtivodecode.

%prep
%setup -q -n %{name}-%{version}pre4

# Add libtool macros to configure.in
sed -i 's/\(AM_MAINTAINER_MODE\)/\1\nLT_PREREQ\nLT_INIT/' configure.in
sed -i 's/\(AC_PROG_INSTALL\)/\1\nAC_PROG_LIBTOOL/' configure.in

# Remove invalid macros from configure.in
sed -i '/Wdeclaration-after-statement/d' configure.in
sed -i '/Wendif-labels/d' configure.in
sed -i '/Werror-implicit-function-declaration/d' configure.in
sed -i '/fno-strict-aliasing/d' configure.in

# Edit Makefile.am to build shared lib
echo 'libtivodecode_a_CFLAGS = $(AM_CFLAGS)' >> Makefile.am
echo 'lib_LTLIBRARIES = libtivodecode.la' >> Makefile.am
echo 'libtivodecode_la_SOURCES=hexlib.c TuringFast.c sha1.c md5.c tivo-parse.c turing_stream.c tivodecoder.c QUTsbox.h TuringMultab.h TuringSbox.h hexlib.h sha1.h md5.h' >> Makefile.am
echo 'libtivodecode_la_LIBADD = libtivodecode.a' >> Makefile.am
sed -i 's/\(.*_DEPENDENCIES.*libtivodecode\).*/\1\.a/' Makefile.am


%build
autoreconf -i -f

%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%doc ChangeLog README

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.*
%doc COPYING

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%exclude %{_libdir}/lib%{name}.la
%exclude %{_libdir}/lib%{name}.a



%changelog
* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.2-0.10.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.2-0.9.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.2-0.8.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.2-0.7.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.2-0.6.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.2-0.5.pre4
- Mass rebuilt for Fedora 19 Features

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.2-0.4.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 29 2009 Bernard Johnson <bjohnson@symetrix.com> - 0.2-0.3.pre4
- License should be BSD and QUALCOMM only
- moved COPYING file to libs package

* Sat Nov 14 2009 Bernard Johnson <bjohnson@symetrix.com> - 0.2-0.2.pre4
- fix package naming
- convert to generate a shared library

* Tue Jun 23 2009 Bernard Johnson <bjohnson@symetrix.com> - 0.2-0.1.pre4.1
- update to correct package naming guidelines

* Wed Jan 21 2009 Bernard Johnson <bjohnson@symetrix.com> - 0.2-0.pre4.1
- initial release
