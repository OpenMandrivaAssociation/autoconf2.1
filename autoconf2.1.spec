%define pkgname	autoconf
%define version	2.13
%define release %mkrel 29

# Define the Fortran compiler
%if %{mdkversion} >= 200600
%define fortran_compiler gfortran
BuildRequires: gcc-gfortran
%else
%define fortran_compiler g77
BuildRequires: gcc-g77
%endif

%define docheck 1
%{?_without_check: %global docheck 0}

Name:		%{pkgname}2.1
Summary:	A GNU tool for automatically configuring source code
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/autoconf/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch

Source:		ftp://ftp.gnu.org/pub/gnu/%{pkgname}/%{pkgname}-%{version}.tar.bz2
Patch0:		autoconf-2.12-race.patch
Patch1:		autoconf-2.13-mawk.patch
Patch2:		autoconf-2.13-notmp.patch
Patch3:		autoconf-fix-for-gcc2.96-patch
Patch4:		autoconf-2.13-versioned-info.patch
Patch5:		autoconf-2.13-automake14.patch
Patch6:		autoconf-2.13-gfortran.patch

Requires(post):	info-install
Requires(preun):	info-install
Requires:	gawk, m4, mktemp
BuildRequires:	texinfo m4
Conflicts:	autoconf2.5 <= 1:2.59-3mdk

# for tests
%if %docheck
BuildRequires:	bison
BuildRequires:	flex
%endif

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to 
specify various configuration options.

You should install Autoconf if you are developing software and you'd
like to use it to create shell scripts which will configure your 
source code packages. If you are installing Autoconf, you will also
need to install the GNU m4 package.

Note that the Autoconf package is not required for the end user who
may be configuring software with an Autoconf-generated script; 
Autoconf is only required for the generation of the scripts, not
their use.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1 -b .parallel
%patch5 -p1 -b .automake14
case %{fortran_compiler} in
*gfortran*)
%patch6 -p1 -b .gfortran
;;
esac

%build
export F77=%{fortran_compiler}
%configure --program-suffix=-%{version}
%make

%if %docheck
make check	# VERBOSE=1
%endif

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

mv $RPM_BUILD_ROOT%{_infodir}/autoconf.info $RPM_BUILD_ROOT%{_infodir}/autoconf-%{version}.info

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f $RPM_BUILD_ROOT%{_infodir}/standards*

cp install-sh $RPM_BUILD_ROOT%{_datadir}/autoconf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info autoconf-%{version}.info

%preun
%_remove_install_info autoconf-%{version}.info

%files
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_datadir}/%{pkgname}
%{_infodir}/*

