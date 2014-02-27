%define NAME	CXSparse
%define major	3
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Name:		cxsparse
Version:	3.1.2
Release:	1
Epoch:		1
Summary:	Direct methods for sparse linear systems
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.cise.ufl.edu/research/sparse/CXSparse/
Source0:	http://www.cise.ufl.edu/research/sparse/CXSparse/versions/%{NAME}-%{version}.tar.gz
BuildRequires:	suitesparse-common-devel >= 4.0.0

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
%define	oldname	%{mklibname %{name} 3.1.1}
%rename		%{oldname}

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

%package -n %{devname}
Summary:	C direct methods for sparse linear systems
Group:		Development/C
Requires:	suitesparse-common-devel >= 4.0.0
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
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
%setup -q -c -n %{name}-%{version}
cd %{NAME}
find . -perm 0600 | xargs chmod 0644
find . -perm 0640 | xargs chmod 0644
mkdir ../SuiteSparse_config
ln -sf %{_includedir}/suitesparse/SuiteSparse_config.* ../SuiteSparse_config

%build
cd %{NAME}
pushd Lib
    %make -f Makefile CC=gcc CFLAGS="%{optflags} -fPIC -I%{_includedir}/suitesparse" INC=
    gcc %{ldflags} -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lm *.o
popd

%install
cd %{NAME}

install -d -m 755 %{buildroot}%{_libdir} 
install -d -m 755 %{buildroot}%{_includedir}/suitesparse 

for f in Lib/*.so*; do
    install -m 755 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    install -m 644 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    install -m 644 $f %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README.txt Doc/*.txt Doc/ChangeLog %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_docdir}/%{name}
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a
