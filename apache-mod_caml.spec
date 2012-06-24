%define		mod_name	mod_caml
%define 	apxs		/usr/sbin/apxs
Summary:	Apache mod_caml module - allows using bytecode compiled ocaml files with apache
Summary(pl):	Modu� Apache'a mod_caml - zapewniaj�cy obs�ug� skompilowanego do bajtkodu ocamla
Name:		apache-%{mod_name}
Version:	1.3.4
Release:	2
Group:		Networking/Daemons
License:	BSD-like
Source0:	http://savannah.nongnu.org/download/modcaml/%{mod_name}-%{version}.tar.gz
# Source-md5:	b21b6a1fee031490a925895b88b3a92f
Patch0:		%{mod_name}-Makefile.diff
URL:		http://merjis.com/developers/mod_caml/
BuildRequires:	apache-devel >= 1.3.3
BuildRequires:	%{apxs}
BuildRequires:	apr-devel
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-pcre-devel
BuildRequires:	ocaml-postgres
Requires(post,preun):	%{apxs}
Requires:	apache >= 1.3.3
Requires:	ocaml >= 3.0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

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
 - DBI library can use Perl DBDs (database drivers)
   [requires Perl4Caml >= 0.3.6].

%description -l pl
mod_caml to zbi�r dowi�za� Objective CAML-a (OCamla) dla API Apache'a.
Umo�liwia uruchamianie skrypt�w CGI napisanych w OCamlu bezpo�rednio
wewn�trz serwera WWW Apache. Umo�liwia jednak znacznie wi�cej:
 - dowi�zanie do dowolnej cz�ci cyklu przetwarzania ��dania,
 - odczyt i modyfikowanie wewn�trznych struktur Apache'a,
 - wsp�dzielenie modu��w kodu mi�dzy procedurami obs�ugi a skryptami,
 - udost�pnia bibliotek� CGI i system szablon�w (umo�lwiaj�cych
   oddzielenie kodu i prezentacji),
 - dzia�a z Apache 1.3 i Apache 2.0,
 - udost�pnia bibliotek� DBI do prostego dost�pu do baz danych,
 - udost�pnia bibliotek� DBI wykorzystuj�c� sterowniki DBD Perla
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
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc COPYING.LIB CHANGES README examples html icons modcaml-example.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd.conf/*.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%{_libdir}/ocaml
%{_datadir}/%{mod_name}
