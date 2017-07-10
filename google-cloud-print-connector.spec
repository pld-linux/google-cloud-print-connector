Summary:	Google Cloud Print Connector
Name:		google-cloud-print-connector
Version:	1.12
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	https://github.com/google/cloud-print-connector/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4196c13a5f912609646d0a9fce643a63
URL:		https://github.com/google/cloud-print-connector
BuildRequires:	avahi-devel
BuildRequires:	cups-devel
BuildRequires:	golang >= 1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/google/cloud-print-connector

%description
Share printers from your Windows, Linux, FreeBSD or OS X computer with
ChromeOS and Android devices, using the Cloud Print Connector. The
Connector is a purpose-built system process. It can share hundreds of
printers on a powerful server, or one printer on a Raspberry Pi.

%prep
%setup -qc

# play with go weird way
install -d src/$(dirname %{import_path})
mv cloud-print-connector-%{version} src/%{import_path}

# to simplify %doc
mv src/%{import_path}/{*.md,LICENSE} .

%build
export GOPATH=$(pwd)

go get -t -v %{import_path}/...
%gobuild %{import_path}/...

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p bin/* $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CONTRIBUTING.md LICENSE
%attr(755,root,root) %{_bindir}/gcp-connector-util
%attr(755,root,root) %{_bindir}/gcp-cups-connector
