%global homedir %{_datadir}/tuskar

Name:	      openstack-tuskar-ui
Version:      XXX
Release:      XXX{?dist}
Summary:	  The UI component for Tuskar

Group:		  Applications/System
License:	  ASL 2.0
URL:		    https://github.com/openstack/tuskar-ui
Source0:	  https://pypi.python.org/packages/source/t/tuskar-ui/tuskar-ui-%{version}.tar.gz

BuildArch:     noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-sphinx >= 1.1.3
BuildRequires: python-flake8
BuildRequires: openstack-dashboard
BuildRequires: os-cloud-config
BuildRequires: python-ironicclient
BuildRequires: python-tuskarclient

# testing deps, not on RHEL
%if 0%{?rhel} == 0
BuildRequires: python-coverage
BuildRequires: python-django-nose
BuildRequires: python-mock
BuildRequires: python-mox
BuildRequires: python-nose
BuildRequires: python-nose-exclude
BuildRequires: python-nose-xcover
BuildRequires: python-openstack-nose-plugin
BuildRequires: python-selenium
%endif

Requires: pytz
Requires: openstack-dashboard
Requires: os-cloud-config
Requires: python-kombu
Requires: python-iso8601
Requires: python-ironicclient
Requires: python-tuskarclient

%description
tuskar-ui is a user interface for Tuskar, a management API for OpenStack
deployments. It is a plugin for OpenStack Horizon.

%prep
%setup -q -n tuskar-ui-%{upstream_version}
rm -rf tuskar_ui.egg-info/

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
export OSLO_PACKAGE_VERSION=%{version}
%{__python2} setup.py build

%install
export OSLO_PACKAGE_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Enable Infrastructure dashboard and disable others
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
cp _10_admin.py.example %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_10_admin.py
cp _20_project.py.example %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_20_project.py
# Keep identity panel enabled to avoid Horizon bug https://bugs.launchpad.net/horizon/+bug/1399126
# cp _30_identity.py.example %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_30_identity.py
cp _50_tuskar.py.example %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_tuskar.py

%files
%doc LICENSE README.rst
%{python_sitelib}/*.egg-info
%{python_sitelib}/tuskar_ui
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_10_admin.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_20_project.py*
# %{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_30_identity.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_tuskar.py*

%check
# don't run tests on rhel
%if 0%{?rhel} == 0
# until django-1.6 support for tests is enabled, disable tests
export PYTHONPATH=$PYTHONPATH:%{_datadir}/openstack-dashboard
# TODO : reenable, We don't have selenium
#./run_tests.sh -N -P
%endif

%changelog
* Tue Apr 21 2015 Jiri Tomasek <jtomasek@redhat.com> - 0.0.1-2
- Cleanup, remove copying static files to openstack-dashboard (it is done automatically by Horizon's systemd scriptlet when httpd restarts)

* Tue Apr 14 2015 Jiri Tomasek <jtomasek@redhat.com> - 0.2.0-6
- do not disable Identity dashboard because of Horizon bug (https://bugs.launchpad.net/horizon/+bug/1399126)

* Tue Mar 24 2015 Jiri Tomasek <jtomasek@redhat.com> 0.2.0-6
- Drop errant requires: on python-pbr

* Tue Oct 28 2014 Jordan OMara <jomara@redhat.com> - 0.2.0-5
- changes to static file locations to more closely mirror horizon (jomara@redhat.com)

* Fri Oct 17 2014 Jordan OMara <jomara@redhat.com> - 0.2.0-2
- conditionally loading test deps (not on RHEL) (jomara@redhat.com)

* Thu Oct 16 2014 Jordan OMara <jomara@redhat.com> - 0.2.0-1
- new sources (0.2.0) (jomara@redhat.com)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-15
- IPMI form patch (jomara@redhat.com)

* Tue May 06 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-14
- updated upstream patch w/ fixed escaping (jomara@redhat.com)

* Thu May 01 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-13
- less confused patches from upstream (jomara@redhat.com)

* Thu May 01 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-12
- Glance logfile & keystone api import fix (jomara@redhat.com)

* Wed Apr 30 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-11
- Upstream instack comment patches

* Wed Apr 09 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-10
- Explicit *.html callout

* Wed Apr 09 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-8
- Github source is not sdist- moving to pypi

* Wed Apr 09 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-7
- Correct upstream source now

* Tue Apr 08 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-6
- Add unit tests

* Tue Apr 08 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-5
- Remove .egg-info in %prep

* Mon Apr 07 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-4
- Fixup from review

* Thu Apr 03 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-3
- Added 0001-Missing-import-url.patch

* Tue Apr 01 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-2
- adding infrastructure files to openstack-dashboard install

* Thu Mar 06 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-1
- initial package
