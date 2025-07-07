import sys
import pytest
from cloudflare_ddns_synology.cli import main

# Global mock for CloudFlare to track instances and behavior
class DummyCF:
    instances = []
    
    def __init__(self, email, api_key, domain, proxied=False):
        self.domain = domain
        self.email = email
        self.api_key = api_key
        self.proxied = proxied
        DummyCF.instances.append(self)
    
    def sync_dns_from_my_ip(self):
        # Default implementation returns True (success)
        return True

@pytest.fixture(autouse=True)
def reset_mock_instances():
    # Reset the instances before each test
    DummyCF.instances = []
    yield
    # Clean up after test if needed
    DummyCF.instances = []

def test_main_runs(monkeypatch, capsys):
    # Simulate CLI args and patch CloudFlare
    import sys
    sys_argv = sys.argv
    sys.argv = [
        'cli',
        '--hostname', 'example.com',
        '--myip', '1.2.3.4',
        '--username', 'test@example.com',
        '--password', 'fake-token'
    ]
    
    # Apply the patch to ensure our mock is used
    monkeypatch.setattr('cloudflare_ddns_synology.cli.CloudFlare', DummyCF)
    monkeypatch.setattr('sys.exit', lambda x: None)  # Don't exit the test process
    
    main()
    
    # Verify the mock was used
    assert len(DummyCF.instances) == 1
    assert DummyCF.instances[0].domain == 'example.com'
    
    out, _ = capsys.readouterr()
    assert 'good' in out  # Now we expect success
    sys.argv = sys_argv

def test_main_with_positional_args(monkeypatch, capsys):
    # Simulate Synology-style positional arguments
    import sys
    sys_argv = sys.argv
    sys.argv = [
        'cli',
        'example.com', 
        '1.2.3.4', 
        'test@example.com', 
        'fake-token'
    ]
    
    # Apply the patch to ensure our mock is used
    monkeypatch.setattr('cloudflare_ddns_synology.cli.CloudFlare', DummyCF)
    monkeypatch.setattr('sys.exit', lambda x: None)  # Don't exit the test process
    
    main()
    
    # Verify the mock was used
    assert len(DummyCF.instances) == 1
    assert DummyCF.instances[0].domain == 'example.com'
    
    out, _ = capsys.readouterr()
    assert 'good' in out  # Now we expect success
    sys.argv = sys_argv

def test_main_runs_with_multiple_domains(monkeypatch, capsys):
    # Simulate CLI args with multiple domains
    import sys
    sys_argv = sys.argv
    sys.argv = [
        'cli',
        '--hostname', 'example.com--subdomain.example.com--another.com',
        '--myip', '1.2.3.4',
        '--username', 'test@example.com',
        '--password', 'fake-token'
    ]
    
    # Apply the patch to ensure our mock is used
    monkeypatch.setattr('cloudflare_ddns_synology.cli.CloudFlare', DummyCF)
    monkeypatch.setattr('sys.exit', lambda x: None)  # Don't exit the test process
    
    main()
    
    # Verify the mock was used
    assert len(DummyCF.instances) == 3
    domains = [instance.domain for instance in DummyCF.instances]
    assert 'example.com' in domains
    assert 'subdomain.example.com' in domains
    assert 'another.com' in domains
    
    out, _ = capsys.readouterr()
    assert 'good' in out  # Now we expect success
    sys.argv = sys_argv

def test_positional_args_with_multiple_domains(monkeypatch, capsys):
    # Simulate Synology-style positional arguments with multiple domains
    import sys
    sys_argv = sys.argv
    sys.argv = [
        'cli',
        'example.com--subdomain.example.com', 
        '1.2.3.4', 
        'test@example.com', 
        'fake-token'
    ]
    
    # Apply the patch to ensure our mock is used
    monkeypatch.setattr('cloudflare_ddns_synology.cli.CloudFlare', DummyCF)
    monkeypatch.setattr('sys.exit', lambda x: None)  # Don't exit the test process
    
    main()
    
    # Verify the mock was used
    assert len(DummyCF.instances) == 2
    domains = [instance.domain for instance in DummyCF.instances]
    assert 'example.com' in domains
    assert 'subdomain.example.com' in domains
    
    out, _ = capsys.readouterr()
    assert 'good' in out  # Now we expect success
    sys.argv = sys_argv

def test_main_fails_gracefully(monkeypatch, capsys):
    # Simulate CLI args with multiple domains
    import sys
    sys_argv = sys.argv
    sys.argv = [
        'cli',
        '--hostname', 'example.com--fail.com',
        '--myip', '1.2.3.4',
        '--username', 'test@example.com',
        '--password', 'fake-token'
    ]
    
    # Create a failing mock version
    class FailingDummyCF(DummyCF):
        def sync_dns_from_my_ip(self): 
            if self.domain == 'fail.com':
                raise Exception("Test failure")
            return True
    
    # Apply the patch to ensure our mock is used
    monkeypatch.setattr('cloudflare_ddns_synology.cli.CloudFlare', FailingDummyCF)
    monkeypatch.setattr('sys.exit', lambda x: None)  # Don't exit the test process
    
    main()
    
    # Verify the mock was used
    assert len(FailingDummyCF.instances) == 2
    domains = [instance.domain for instance in FailingDummyCF.instances]
    assert 'example.com' in domains
    assert 'fail.com' in domains
    
    out, err = capsys.readouterr()
    assert '911' in out  # Error code expected
    assert 'Error updating fail.com: Test failure' in err
    
    sys.argv = sys_argv
