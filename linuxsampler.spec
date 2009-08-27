%define	major	3
%define	libname	%mklibname %name %major
%define	develname %mklibname %name -d

Name:          linuxsampler
Summary:       Professional grade software audio sampler
Version:       1.0.0
Release:       %mkrel 1
License:       GPL
Group:	       Sound
Source0:       %{name}-%{version}.tar.bz2
URL: 	       http://www.linuxsampler.org/
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: libgig-devel >= 3.3.0
BuildRequires: libjack-devel
BuildRequires: dssi-devel
BuildRequires: sqlite3-devel
BuildRequires: lv2core-devel
#BuildRequires: arts-devel

%description
LinuxSampler is a professional grade software audio sampler 
that aims to deliver performance and features at par with 
hardware sampler devices

%files
%defattr(-,root,root)
%_bindir/linuxsampler
%_mandir/man1/linuxsampler.1.*
%_prefix/README.urpmi
%_localstatedir/lib/%{name}/*.db
%dir %_libdir/%{name}/plugins

#--------------------------------------------------------------------

%package -n	%libname
Group: 		System/Libraries
Summary: 	Libraries for %name
Provides: 	lib%name = %version-%release

%description -n %libname
Librairies from %name

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -n %libname
%defattr(-,root,root)
%_libdir/linuxsampler/liblinuxsampler.so.%{major}*

#--------------------------------------------------------------------

%package -n	%develname
Group: 		Development/Other
Summary: 	Libraries for %name
Requires:	%libname = %version-%release
Provides:	lib%name-devel = %version-%release
Provides: 	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}%{name}1-devel

%description -n	%develname
Development libraries from %name

%files -n %develname
%defattr (-,root,root)
%_includedir/%name/*.h
%_includedir/%name/common/*.h
%_includedir/%name/drivers/*.h
%_includedir/%name/drivers/audio/*.h
%_includedir/%name/drivers/midi/*.h
%_includedir/%name/effects/*.h
%_includedir/%name/engines/*.h
%_includedir/%name/plugins/*.h
%_libdir/pkgconfig/%name.pc
%_libdir/dssi/*.a
%_libdir/dssi/*.la
%_libdir/dssi/*.so
%_libdir/lv2/linuxsampler.lv2/*.a
%_libdir/lv2/linuxsampler.lv2/*.la
%_libdir/lv2/linuxsampler.lv2/*.so
%_libdir/lv2/linuxsampler.lv2/*.ttl
%_libdir/%name/liblinuxsampler.a
%_libdir/%name/liblinuxsampler.la
%_libdir/%name/liblinuxsampler.so

#--------------------------------------------------------------------

%prep
%setup -q -n %name-%version

%build
%configure2_5x
%make

%install
make DESTDIR=%buildroot  install

cat > %buildroot/%_prefix/README.urpmi <<EOF

WARNING
-------
LinuxSampler is licensed under the GNU GPL with the exception that 
USAGE of the source code, libraries and applications FOR COMMERCIAL 
HARDWARE OR SOFTWARE PRODUCTS IS NOT ALLOWED  without prior written 
permission by the LinuxSampler authors. If you have questions on the 
subject, that are not yet covered by the FAQ, please contact us.

EOF

%clean

