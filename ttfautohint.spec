#
# Conditional build:
%bcond_with	qt5	# Qt 5 instead of Qt 4
#
Summary:	Auto-generating hints for TrueType fonts
Summary(pl.UTF-8):	Automatyczne generowanie hintingu dla fontów TrueType
Name:		ttfautohint
Version:	1.5
Release:	1
License:	FreeType License or GPL v2+
Group:		Applications/Graphics
Source0:	http://download.savannah.gnu.org/releases/freetype/%{name}-%{version}.tar.gz
# Source0-md5:	39d6aa578c66c9bb518a9feb1b85b385
URL:		http://freetype.org/
BuildRequires:	freetype-devel >= 1:2.4.5
BuildRequires:	harfbuzz-devel >= 0.9.19
BuildRequires:	pkgconfig >= 1:0.24
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5.0
BuildRequires:	Qt5Gui-devel >= 5.0
BuildRequires:	Qt5Widgets-devel >= 5.0
BuildRequires:	qt5-build >= 5.0
%else
BuildRequires:	QtCore-devel >= 4.8
BuildRequires:	QtGui-devel >= 4.8
BuildRequires:	qt4-build >= 4.6
%endif
Requires:	freetype >= 1:2.4.5
Requires:	harfbuzz >= 0.9.19
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qtmajor	%{?with_qt5:5}%{!?with_qt5:4}

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

%package gui
Summary:	GUI application to replace hints in a TrueType font
Summary(pl.UTF-8):	Graficzna aplikacja do podmiany reguł hintingu w fontach TrueType
Group:		X11/Applications/Graphics
%if %{without qt5}
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
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# requirements to automatically install man pages are insane - do it manually
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p frontend/ttf*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog FTL.TXT NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/ttfautohint
%{_mandir}/man1/ttfautohint.1*

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ttfautohintGUI
%{_mandir}/man1/ttfautohintGUI.1*
