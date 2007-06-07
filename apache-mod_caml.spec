# TODO
# - fix build for apache 2.2
%define		mod_name	mod_caml
%define 	apxs		/usr/sbin/apxs
Summary:	Apache mod_caml module - allows using bytecode compiled ocaml files with apache
Summary(pl.UTF-8):	Moduł Apache'a mod_caml - zapewniający obsługę skompilowanego do bajtkodu ocamla
Name:		apache-%{mod_name}
Version:	1.3.4
Release:	2
License:	BSD-like
Group:		Networking/Daemons
Source0:	http://savannah.nongnu.org/download/modcaml/%{mod_name}-%{version}.tar.gz
# Source0-md5:	b21b6a1fee031490a925895b88b3a92f
Patch0:		%{mod_name}-Makefile.diff
URL:		http://merjis.com/developers/mod_caml/
BuildRequires:	apache-apxs >= 2.0
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-pcre-devel
BuildRequires:	ocaml-postgres
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Requires:	ocaml >= 3.0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

# I don't understand it but it is neccessary if one strips
# it, it won't work. Help welcome.
%define		_noautostrip	.*\/mod_caml.so

%description
mod_caml is a set of Objective CAML (OCaml) bindings for the Apache
API. It allows you to run CGI scripts written in OCaml directly inside
the Apache webserver. However, it is much much more than just that:
 - Bind to any part of the Apache request cycle.
 - Read and modify internal Apache structures.
 - Share modules of code between handlers and scripts.
 - CGI library and templating system (allows separation of code and
   presentation).
 - Works with Apache 1.3 and Apache 2.0.
 - DBI library for simple database access.
 - DBI library can use Perl DBDs (database drivers) [requires Perl4Caml
   >= 0.3.6].

%description -l pl.UTF-8
mod_caml to zbiór dowiązań Objective CAML-a (OCamla) dla API Apache'a.
Umożliwia uruchamianie skryptów CGI napisanych w OCamlu bezpośrednio
wewnątrz serwera WWW Apache. Umożliwia jednak znacznie więcej:
 - dowiązanie do dowolnej części cyklu przetwarzania żądania,
 - odczyt i modyfikowanie wewnętrznych struktur Apache'a,
 - współdzielenie modułów kodu między procedurami obsługi a skryptami,
 - udostępnia bibliotekę CGI i system szablonów (umożlwiających
   oddzielenie kodu i prezentacji),
 - działa z Apache 1.3 i Apache 2.0,
 - udostępnia bibliotekę DBI do prostego dostępu do baz danych,
 - udostępnia bibliotekę DBI wykorzystującą sterowniki DBD Perla
   (wymaga pakietu Perl4Caml >= 0.3.6).

%prep
%setup -q -n %{mod_name}-%{version}
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc COPYING.LIB CHANGES README examples html icons modcaml-example.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%{_libdir}/ocaml
%{_datadir}/%{mod_name}
