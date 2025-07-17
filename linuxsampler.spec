%global	_disable_ld_no_undefined 1
%global	_disable_lto 1

%define		major	8
%define		libname	%mklibname %{name}
%define		oldlibname	%mklibname %{name} 6
%define		develname %mklibname %{name} -d

Summary:	Professional grade software audio sampler
Name:	linuxsampler
Version:	2.4.0
Release:	1
License:	GPLv2+
Group:	Sound/Midi
Url:		https://www.linuxsampler.org/
Source0:	https://download.linuxsampler.org/packages/linuxsampler-%{version}.tar.bz2
#Patch0:	linuxsampler-0001-aarch64-fix.patch
Patch1:		linuxsampler-2.2.0-compile.patch
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	which
BuildRequires:	perl(XML::Parser)
BuildRequires:	pkgconfig(dssi)
BuildRequires:	pkgconfig(gig) >= 4.5.0
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(lv2) >= 1.12
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(sqlite3) >= 3.3
Requires:	gig
Requires:	jackit
Requires:	liblscp
Requires:	lv2
Requires:	%{libname} = %{version}-%{release}

%description
LinuxSampler is a professional grade software audio sampler that aims to
deliver performance and features at par with hardware sampler devices.

%files
%doc README.urpmi NEWS
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
%rename %{oldlibname}

%description -n %{libname}
Libraries from %{name}.

%files -n %{libname}
%{_libdir}/%{name}/lib%{name}.so.%{major}{,.*}
%{_libdir}/lv2/%{name}.lv2/*.ttl
%{_libdir}/lv2/%{name}.lv2/%{name}.so
%{_libdir}/dssi/%{name}.so

#--------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}%{name}-devel < %{version}-%{release}

%description -n	%{develname}
Development libraries from %{name}.

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
%{_libdir}/%{name}/lib%{name}.so

#--------------------------------------------------------------------

%prep
%autosetup -p1

export CXXFLAGS="%{optflags} -std=c++17"
[ -f Makefile.svn ] && make -f Makefile.svn


%build
%configure \
	--disable-static \
	--disable-arts-driver \
	--disable-artstest \
	--disable-midishare-driver \
	--enable-signed-triang-algo=intmathabs \
	--enable-unsigned-triang-algo=diharmonic

[ -f Makefile.svn ] && make parser
%make_build

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
