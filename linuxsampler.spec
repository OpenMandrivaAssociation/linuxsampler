%define	major	1
%define	libname	%mklibname %name %major

Name:          linuxsampler
Summary:       Professional grade software audio sampler
Version:       0.5.1
Release:       %mkrel 3
License:       GPL
Group:	       Sound
Source0:       %{name}-%{version}.tar.bz2
URL: 	       http://www.linuxsampler.org/
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: libgig-devel
BuildRequires: arts-devel

%description
LinuxSampler is a professional grade software audio sampler 
that aims to deliver performance and features at par with 
hardware sampler devices

%files
%defattr(-,root,root)
%_bindir/linuxsampler
%_mandir/man1/linuxsampler.1.lzma
%_prefix/README.urpmi

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
%_libdir/linuxsampler/liblinuxsampler.so.1
%_libdir/linuxsampler/liblinuxsampler.so.1.1.0

#--------------------------------------------------------------------

%package -n	%libname-devel
Group: 		Development/Other
Summary: 	Libraries for %name
Requires:	%libname = %version-%release
Provides:	lib%name-devel = %version-%release
Provides: 	%{name}-devel = %{version}-%{release}

%description -n	%libname-devel
Development libraries from %name

%files -n %libname-devel
%defattr (-,root,root)
%dir %_includedir/linuxsampler
%_includedir/linuxsampler/*.h
%dir %_includedir/linuxsampler/common
%_includedir/linuxsampler/common/*.h
%dir %_includedir/linuxsampler/drivers
%_includedir/linuxsampler/drivers/*.h
%dir %_includedir/linuxsampler/drivers/audio
%_includedir/linuxsampler/drivers/audio/*.h
%dir %_includedir/linuxsampler/drivers/midi
%_includedir/linuxsampler/drivers/midi/*.h
%dir %_includedir/linuxsampler/engines
%_includedir/linuxsampler/engines/*.h
%dir %_includedir/linuxsampler/plugins 
%_includedir/linuxsampler/plugins/*.h
%_libdir/pkgconfig/linuxsampler.pc
%dir %_libdir/linuxsampler
%_libdir/linuxsampler/liblinuxsampler.a
%_libdir/linuxsampler/liblinuxsampler.la
%_libdir/linuxsampler/liblinuxsampler.so

#--------------------------------------------------------------------

%prep
%setup -q -n %name-%version

%build
%configure


make

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

