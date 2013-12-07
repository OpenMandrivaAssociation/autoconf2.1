%define pkgname	autoconf

# Define the Fortran compiler
%define fortran_compiler gfortran
BuildRequires: gcc-gfortran

%define docheck 1
%{?_without_check: %global docheck 0}

Name:		%{pkgname}2.1
Summary:	A GNU tool for automatically configuring source code
Version:	2.13
Release:	38
Epoch:		1
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/autoconf/
BuildArch:	noarch

Source:		ftp://ftp.gnu.org/pub/gnu/%{pkgname}/%{pkgname}-%{version}.tar.bz2
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

mv $RPM_BUILD_ROOT%{_infodir}/autoconf.info $RPM_BUILD_ROOT%{_infodir}/autoconf-%{version}.info

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f $RPM_BUILD_ROOT%{_infodir}/standards*

cp install-sh $RPM_BUILD_ROOT%{_datadir}/autoconf

%files
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_datadir}/%{pkgname}
%{_infodir}/*



%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.13-32mdv2011.0
+ Revision: 662895
- mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.13-31mdv2011.0
+ Revision: 603480
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.13-30mdv2010.1
+ Revision: 520010
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.13-29mdv2010.0
+ Revision: 413143
- rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1:2.13-28mdv2009.0
+ Revision: 220469
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot
- fix prereq

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Jun 14 2007 Christiaan Welvaart <spturtle@mandriva.org> 1:2.13-26mdv2008.0
+ Revision: 39538
- drop support for wrapper script to allow renaming autoconf2.5 to autoconf

* Tue Jun 05 2007 Christiaan Welvaart <spturtle@mandriva.org> 1:2.13-25mdv2008.0
+ Revision: 35330
- bunzip2 autoconf-fix-for-gcc2.96-patch


* Sun Jul 02 2006 Stefan van der Eijk <stefan@mandriva.org> 2.13-25
- %%mkrel

* Fri Aug 12 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.13-24mdk
- reintroduce the gfortran fallback patch from abel

* Tue Jul 19 2005 Abel Cheung <deaddog@mandriva.org> 2.13-23mdk
- Revert everything

* Tue Jul 19 2005 Abel Cheung <deaddog@mandriva.org> 1:2.13-22mdk
- Disable patch3 (for gcc 2.96 only?)
- Patch6: Attempt to use gfortran as last resort for fortran compiler

* Sat May 22 2004 Abel Cheung <deaddog@deaddog.org> 2.13-21mdk
- Patch5: invoke automake-1.4 and aclocal-1.4 instead of random
  version of automake/aclocal in autoreconf
- Do make check by default

* Fri May 14 2004 Abel Cheung <deaddog@deaddog.org> 2.13-20mdk
- THE BIG MOVE
- wrapper script moved to 2.5x package
- Add `--with check' option to enable `make check'

* Tue Aug 19 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-19mdk
- own /usr/lib/autoconf, thx to markus pilzecker <pilzecker at free.fr>

* Mon Aug 11 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-18mdk
- autoconf-2.13-talk-about-2.5x-in-info (#4698)

