#
# Conditional build:
%bcond_with	doc	# API documentation
%bcond_with	tests	# unit tests, nonesense dependency loop with matplotlib

%define		module	contourpy
Summary:	Python library for calculating contours of 2D quadrilateral grids
Summary(pl.UTF-8):	Biblioteka Pythona do obliczania konturów siatek czworokątnych 2D
Name:		python3-%{module}
Version:	1.3.3
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/contourpy/
Source0:	https://files.pythonhosted.org/packages/source/c/contourpy/%{module}-%{version}.tar.gz
# Source0-md5:	3592ea8e491e04fc7a87721e0beb7b0e
URL:		https://pypi.org/project/contourpy/
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	meson >= 1.2.0
BuildRequires:	python3-devel >= 1:3.11
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-meson-python >= 0.13.1
BuildRequires:	python3-pybind11 >= 2.13.2
%if %{with tests}
BuildRequires:	python3-matplotlib
BuildRequires:	python3-numpy >= 1.25
BuildRequires:	python3-wurlitzer
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-matplotlib
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	sphinx-pdg-3 >= 7.2
%endif
Requires:	python3-modules >= 1:3.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ContourPy is a Python library for calculating contours of 2D
quadrilateral grids. It is written in C++11 and wrapped using
pybind11.

%description -l pl.UTF-8
Contourpy to biblioteka Pythona do obliczania konturów siatek
czworokątnych 2D. Jest napisana w C++11 i obudowana przy użyciu
pybind11.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
# array-bounds warning in pybind11 code
CXXFLAGS="%{rpmcxxflags} -Wno-error=array-bounds"
%py3_build_pyproject

%if %{with tests} || %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
%endif

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3-test \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md README_simple.md
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/*.pyi
%{py3_sitedir}/%{module}/py.typed
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}/util
%{py3_sitedir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
