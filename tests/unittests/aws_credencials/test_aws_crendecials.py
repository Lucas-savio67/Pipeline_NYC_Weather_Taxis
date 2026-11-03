import pytest

from config.aws_credencials import CredencialsErrors, load_aws_credencials

def test_abscent_aws_credencial(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "teste")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "teste")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.delenv("AWS_BUCKET_NAME", raising=False)

    with pytest.raises(CredencialsErrors, match="bucket_name"):
        load_aws_credencials()