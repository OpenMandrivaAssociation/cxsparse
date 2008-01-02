%define epoch		0

%define name		cxsparse
%define NAME		CXSparse
%define version		2.2.1
%define release		%mkrel 4
%define major		%{version}
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Direct methods for sparse linear systems
Group:		System/Libraries
License:	LGPL
URL:		http://www.cise.ufl.edu/research/sparse/CXSparse/
Source0:	http://www.cise.ufl.edu/research/sparse/CXSparse/%{NAME}-%{version}.tar.gz
Source1:	http://www.cise.ufl.edu/research/sparse/ufconfig/UFconfig-3.1.0.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
CSparse is a package of direct methods for sparse linear systems written
to complement the book "Direct Methods for Sparse Linear Systems", by
Timothy A. Davis. The algorithms in CSparse have been chosen with 
five goals in mind:

(1) they must embody much of the theory behind sparse matrix algorithms,
(2) they must be either asymptotically optimal in their run time and memory
    usage or be fast in practice,
(3) they must be concise so as to be easily understood and short enough to
    print in the book,
(4) they must cover a wide spectrum of matrix operations, and
(5) they must be accurate and robust.

The focus is on direct methods; iterative methods and solvers for
eigenvalue problems are beyond the scope of this package.

CXSparse is a version of CSparse that operates on both real and complex
matrices, using either int or UF_long integers.

%package -n %{libname}
Summary:	Library of direct methods for sparse linear systems
Group:		System/Libraries
Provides:	%{libname} = %{epoch}:%{version}-%{release}

%description -n %{libname}
CSparse is a package of direct methods for sparse linear systems written
to complement the book "Direct Methods for Sparse Linear Systems", by
Timothy A. Davis. The algorithms in CSparse have been chosen with 
five goals in mind:

(1) they must embody much of the theory behind sparse matrix algorithms,
(2) they must be either asymptotically optimal in their run time and memory
    usage or be fast in practice,
(3) they must be concise so as to be easily understood and short enough to
    print in the book,
(4) they must cover a wide spectrum of matrix operations, and
(5) they must be accurate and robust.

The focus is on direct methods; iterative methods and solvers for
eigenvalue problems are beyond the scope of this package.

CXSparse is a version of CSparse that operates on both real and complex
matrices, using either int or UF_long integers.

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{develname}
Summary:	C direct methods for sparse linear systems
Group:		Development/C
Requires:	suitesparse-common-devel >= 3.0.0
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname %name 2 -d
Obsoletes:	%mklibname %name 2 -d -s

%description -n %{develname}
CSparse is a package of direct methods for sparse linear systems written
to complement the book "Direct Methods for Sparse Linear Systems", by
Timothy A. Davis. The algorithms in CSparse have been chosen with 
five goals in mind:

(1) they must embody much of the theory behind sparse matrix algorithms,
(2) they must be either asymptotically optimal in their run time and memory
    usage or be fast in practice,
(3) they must be concise so as to be easily understood and short enough to
    print in the book,
(4) they must cover a wide spectrum of matrix operations, and
(5) they must be accurate and robust.

The focus is on direct methods; iterative methods and solvers for
eigenvalue problems are beyond the scope of this package.

CXSparse is a version of CSparse that operates on both real and complex
matrices, using either int or UF_long integers.

This package contains the files needed to develop applications which
use %{name}.

%prep
%setup -q -c 
%setup -q -c -a 0 -a 1
%setup -q -D -T -n %{name}-%{version}/%{NAME}

%build
pushd Lib
    %make -f Makefile CC=%__cc CFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/suitesparse" INC=
    %__cc -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lm *.o
popd

%install
%__rm -rf %{buildroot}

%__install -d -m 755 %{buildroot}%{_libdir} 
%__install -d -m 755 %{buildroot}%{_includedir}/suitesparse 

for f in Lib/*.so*; do
    %__install -m 755 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    %__install -m 644 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    %__install -m 644 $f %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

%__ln_s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

%__install -d -m 755 %{buildroot}%{_docdir}/%{name}
%__install -m 644 README.txt Doc/*.txt Doc/ChangeLog %{buildroot}%{_docdir}/%{name}

%clean
%__rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_docdir}/%{name}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
