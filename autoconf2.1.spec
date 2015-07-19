%define pkgname	autoconf

# Define the Fortran compiler
%define fortran_compiler gfortran
BuildRequires: gcc-gfortran

%define docheck 1
%{?_without_check: %global docheck 0}

Name:		%{pkgname}2.1
Summary:	A GNU tool for automatically configuring source code
Version:	2.13
Release:	43
Epoch:		1
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/autoconf/
BuildArch:	noarch

Source0:	ftp://ftp.gnu.org/pub/gnu/%{pkgname}/%{pkgname}-%{version}.tar.bz2
Source1:	autoconf2.1.rpmlintrc
Patch0:		autoconf-2.12-race.patch
Patch1:		autoconf-2.13-mawk.patch
Patch2:		autoconf-2.13-notmp.patch
Patch3:		autoconf-fix-for-gcc2.96-patch
Patch4:		autoconf-2.13-versioned-info.patch
Patch5:		autoconf-2.13-automake14.patch
Patch6:		autoconf-2.13-gfortran.patch

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
%makeinstall

mv %{buildroot}%{_infodir}/autoconf.info %{buildroot}%{_infodir}/autoconf-%{version}.info

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f %{buildroot}%{_infodir}/standards*

cp install-sh %{buildroot}%{_datadir}/autoconf

%files
%doc README
%{_bindir}/*
%{_datadir}/%{pkgname}
%{_infodir}/*
