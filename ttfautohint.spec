#
# Conditional build:
%bcond_with	qt4		# Qt 4 instead of Qt 5
%bcond_without	static_libs	# static library
#
Summary:	Auto-generating hints for TrueType fonts
Summary(pl.UTF-8):	Automatyczne generowanie hintingu dla fontów TrueType
Name:		ttfautohint
Version:	1.8.4
Release:	1
License:	FreeType License or GPL v2+
Group:		Applications/Graphics
Source0:	http://download.savannah.gnu.org/releases/freetype/%{name}-%{version}.tar.gz
# Source0-md5:	5e5b320217909ddfc9ba527cbf7ec823
URL:		http://freetype.org/
BuildRequires:	freetype-devel >= 1:2.4.5
BuildRequires:	harfbuzz-devel >= 2.4.0
BuildRequires:	pkgconfig >= 1:0.24
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4.8
BuildRequires:	QtGui-devel >= 4.8
BuildRequires:	qt4-build >= 4.8
%else
BuildRequires:	Qt5Core-devel >= 5.0
BuildRequires:	Qt5Gui-devel >= 5.0
BuildRequires:	Qt5Widgets-devel >= 5.0
BuildRequires:	qt5-build >= 5.0
%endif
Requires:	freetype >= 1:2.4.5
Requires:	harfbuzz >= 2.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qtmajor	%{?with_qt4:4}%{!?with_qt4:5}

%description
This project provides a utility which takes a TrueType font as the
input, remove its hinting bytecode instructions (if any), and return a
new font where all glyphs are bytecode hinted using the information
given by FreeType's autohinting module. The idea is to provide the
same quality of the autohinter on platforms which don't use FreeType.

%description -l pl.UTF-8
Ten projekt zapewnia narzędzie przyjmujące na wejściu fonty TrueType,
usuwające z nich instrukcje bajtkodowe hintingu (jeśli są) i tworzące
nowy font, w którym wszystkie glify wykorzystują hinting utworzony
przy użyciu modułu autohintingu z FreeType. Celem jest zapewnienie tej
samej jakości, którą daje autohinter, na platformach nie
wykorzystujących FreeType.

%package devel
Summary:	Header files for ttfautohint library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ttfautohint
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	freetype-devel >= 1:2.4.5
Requires:	harfbuzz-devel >= 2.4.0

%description devel
Header files for ttfautohint automatic font hinting library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ttfautohint, służącej do automatycznego
hintingu fontów.

%package static
Summary:	Static ttfautohint library
Summary(pl.UTF-8):	Statyczna biblioteka ttfautohint
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ttfautohint library.

%description static -l pl.UTF-8
Statyczna biblioteka ttfautohint.

%package gui
Summary:	GUI application to replace hints in a TrueType font
Summary(pl.UTF-8):	Graficzna aplikacja do podmiany reguł hintingu w fontach TrueType
Group:		X11/Applications/Graphics
%if %{with qt4}
Requires:	QtGui >= 4.8
%endif
Requires:	freetype >= 1:2.4.5

%description gui
GUI application to replace hints in a TrueType font. The new hints are
based on FreeType's auto-hinter.

%description gui -l pl.UTF-8
Graficzna aplikacja do podmiany reguł hintingu w fontach TrueType.
Nowe reguły są oparte na auto-hinterze z FreeType.

%prep
%setup -q

%build
%configure \
	MOC=/usr/bin/moc-qt%{qtmajor} \
	QMAKE=/usr/bin/qmake-qt%{qtmajor} \
	QTDIR=%{_libdir}/qt%{qtmajor} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libttfautohint.la

# install (dist) man pages manually - requirements to automatically install them
# are insane ($DISPLAY + ImageMagick + inkscape + pandoc + xelatex + NotoSans fonts)
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p frontend/ttf*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog FTL.TXT NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/ttfautohint
%attr(755,root,root) %{_libdir}/libttfautohint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libttfautohint.so.1
%{_mandir}/man1/ttfautohint.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libttfautohint.so
%{_includedir}/ttfautohint*.h
%{_pkgconfigdir}/ttfautohint.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libttfautohint.a
%endif

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ttfautohintGUI
%{_mandir}/man1/ttfautohintGUI.1*
