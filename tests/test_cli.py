from cloudflare_ddns_synology.cli import main

def test_main_runs(monkeypatch, capsys):
    # Simulate CLI args and patch CloudflareDDNS
    import sys
    sys_argv = sys.argv
    sys.argv = [
        'cli',
        '--hostname', 'example.com',
        '--myip', '1.2.3.4',
        '--username', 'test@example.com',
        '--password', 'fake-token'
    ]
    class DummyCF:
        def __init__(self, **kwargs): pass
        def update_dns(self): pass
    monkeypatch.setattr('cloudflare_ddns.cloudflare_ddns.CloudflareDDNS', DummyCF)
    main()
    out, _ = capsys.readouterr()
    assert 'good' in out
    sys.argv = sys_argv
