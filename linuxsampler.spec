%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define	major	5
%define	libname	%mklibname %{name} %major
%define	develname %mklibname %{name} -d

Name:		linuxsampler
Summary:	Professional grade software audio sampler
Version:	2.2.0
Release:	1
License:	GPLv2
Group:		Sound/Midi
URL:		http://www.linuxsampler.org/
Source0:	http://download.linuxsampler.org/packages/linuxsampler-%{version}.tar.bz2
BuildRequires:	pkgconfig(gig)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(dssi)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	pkgconfig(lv2) >= 1.12
BuildRequires:	perl(XML::Parser)
BuildRequires:	flex

Requires:	jackit
Requires:	liblscp
Requires:	gig
Requires:	lv2
Requires:	%{libname} = %{version}-%{release}

%description
LinuxSampler is a professional grade software audio sampler
that aims to deliver performance and features at par with
hardware sampler devices

%files
%doc README.urpmi
%{_bindir}/%{name}
%{_bindir}/lscp
%{_bindir}/ls_instr_script
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/lscp.1.*
%{_localstatedir}/lib/%{name}/*.db
%dir %{_libdir}/%{name}/plugins

#--------------------------------------------------------------------

%package -n %{libname}
Group:		System/Libraries
Summary:	Libraries for %{name}
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
Libraries from %{name}

%files -n %{libname}
%{_libdir}/%{name}/lib%{name}.so.%{major}{,.*}
%{_libdir}/lv2/%{name}.lv2/*.ttl

#--------------------------------------------------------------------

%package -n %{develname}
Group:		Development/Other
Summary:	Libraries for %{name}
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}%{name}1-devel <= %{version}-%{release}

%description -n	%{develname}
Development libraries from %{name}

%files -n %{develname}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/common/*.h
%{_includedir}/%{name}/drivers/*.h
%{_includedir}/%{name}/drivers/audio/*.h
%{_includedir}/%{name}/drivers/midi/*.h
%{_includedir}/%{name}/effects/*.h
%{_includedir}/%{name}/engines/*.h
%{_includedir}/%{name}/plugins/*.h
%{_includedir}/%{name}/scriptvm/ScriptVM.h
%{_includedir}/%{name}/scriptvm/ScriptVMFactory.h
%{_includedir}/%{name}/scriptvm/common.h
%{_libdir}/pkgconfig/%{name}.pc
#{_libdir}/dssi/*.so
%{_libdir}/lv2/%{name}.lv2/*.so
%{_libdir}/%{name}/lib%{name}.so

#--------------------------------------------------------------------

%prep
%setup -q
export CXXFLAGS="%{optflags} -std=c++17"
%autopatch -p1
[ -f Makefile.cvs ] && make -f Makefile.svn

%build
%configure2_5x
[ -f Makefile.svn ] && make parser
%make
make docs

%install
%make_install

cat > README.urpmi <<EOF
WARNING
-------
LinuxSampler is licensed under the GNU GPL with the exception that 
USAGE of the source code, libraries and applications FOR COMMERCIAL 
HARDWARE OR SOFTWARE PRODUCTS IS NOT ALLOWED  without prior written 
permission by the LinuxSampler authors. If you have questions on the 
subject, that are not yet covered by the FAQ, please contact us. 
EOF

find %{buildroot} -regex ".*\(a\|la\)$" -delete




%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2011.0
+ Revision: 620242
- the mass rebuild of 2010.0 packages

* Thu Aug 27 2009 Emmanuel Andry <eandry@mandriva.org> 1.0.0-1mdv2010.0
+ Revision: 421786
- New version 1.0.0
- new major 3
- drop arts support

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat Dec 15 2007 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.5.1-1mdv2008.1
+ Revision: 120284
- import linuxsampler


