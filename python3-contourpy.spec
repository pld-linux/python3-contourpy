#
# Conditional build:
%bcond_with	doc	# API documentation
%bcond_with	tests	# unit tests, nonesense dependency loop with matplotlib

%define		module	contourpy
Summary:	Python library for calculating contours of 2D quadrilateral grids
Name:		python3-%{module}
Version:	1.3.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/contourpy/
Source0:	https://files.pythonhosted.org/packages/source/c/contourpy/%{module}-%{version}.tar.gz
# Source0-md5:	06a4ae6ab30b855514797cac7073ed08
URL:		https://pypi.org/project/contourpy/
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-meson-python
BuildRequires:	python3-pybind11
%if %{with tests}
BuildRequires:	python3-matplotlib
BuildRequires:	python3-wurlitzer
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ContourPy is a Python library for calculating contours of 2D
quadrilateral grids. It is written in C++11 and wrapped using
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
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
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
