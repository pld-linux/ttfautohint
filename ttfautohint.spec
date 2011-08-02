Summary:	Auto-generating hints for TrueType fonts
Summary(pl.UTF-8):	Automatyczne generowanie hintingu dla fontów TrueType
Name:		ttfautohint
Version:	0.2
Release:	1
License:	FreeType License or GPL v2+
Group:		Applications
Source0:	http://downloads.sourceforge.net/freetype/%{name}-%{version}.tar.gz
# Source0-md5:	423a4b615f8d003f3a26129af371c002
URL:		http://freetype.org/
BuildRequires:	freetype-devel >= 1:2.4.5
Requires:	freetype >= 1:2.4.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q

%build
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog FTL.TXT NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/ttfautohint
%{_mandir}/man1/ttfautohint.1*
