%define		_modname	pam_auth
Summary:	%{_modname} - authenticate someone using PAM
Summary(pl.UTF-8):   %{_modname} - uwierzytelnianie przy użyciu PAM
Name:		php-%{_modname}
Version:	0.4
Release:	0.1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://www.math.ohio-state.edu/~ccunning/pam_auth/%{_modname}-%{version}-4.3.tar.gz
# Source0-md5:	cc757d76194b1b5d41bfa74cfe6275df
URL:		http://www.math.ohio-state.edu/~ccunning/pam_auth/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pam_auth is a simple standalone PHP module that contains exactly one
function. This simple, yet magical function, allows you to
authenticate someone using PAM. It's painless to use, and returns
either true or false (with an error).

%description -l pl.UTF-8
pam_auth to prosty samodzielny moduł PHP zawierający dokładnie jedną
funkcję. Ta prosta, lecz magiczna funkcja pozwala uwierzytelnić kogoś
przy użyciu PAM. Jest bezbolesna w użyciu i zwraca true lub false
(wraz z błędem).

%prep
%setup -q -c

%build
cd %{_modname}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}/{FAQ,README}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
